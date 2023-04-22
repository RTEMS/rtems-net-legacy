#include <machine/rtems-bsd-kernel-space.h>

/*
 *
 * RTEMS Project (https://www.rtems.org/)
 *
 * Copyright (c) 2021 Vijay Kumar Banerjee <vijay@rtems.org>.
 * All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <rtems.h>
#include <rtems/error.h>
#include <rtems/rtems_bsdnet.h>

#include <rtems/rtems_bsdnet_internal.h>

#include <unistd.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <errno.h>

#include "rtems_syscall.h"

static int setup_socketpair(int listener, int *socket_vector)
{
  union {
    struct sockaddr addr;
    struct sockaddr_in inaddr;
  } a;
  int reuse = 1;
  socklen_t addrlen = sizeof(a.inaddr);

  memset(&a, 0, sizeof(a));
  a.inaddr.sin_family = AF_INET;
  a.inaddr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  a.inaddr.sin_port = 0;

  if (setsockopt(listener, SOL_SOCKET, SO_REUSEADDR,
       (char*) &reuse, (socklen_t) sizeof(reuse)) == -1) {
    return 1;
  }

  if  (bind(listener, &a.addr, sizeof(a.inaddr)) == -1) {
    return 1;
  }

  memset(&a, 0, sizeof(a));
  if  (getsockname(listener, &a.addr, &addrlen) == -1) {
    return 1;
  }

  a.inaddr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  a.inaddr.sin_family = AF_INET;

  if (listen(listener, 1) == -1) {
    return 1;
  }

  socket_vector[0] = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (socket_vector[0] == -1) {
    return 1;
  }

  if (connect(socket_vector[0], &a.addr, sizeof(a.inaddr)) == -1) {
    return 1;
  }

  socket_vector[1] = accept(listener, NULL, NULL);
  if (socket_vector[1] == -1) {
    return 1;
  }

  close(listener);
  return 0;
}

/* Fake socketpair() support with a loopback TCP socket */
int
socketpair(int domain, int type, int protocol, int *socket_vector)
{
  int listener;
  int saved_errno;

  if (socket_vector == NULL) {
    errno = EINVAL;
    return -1;
  }
  socket_vector[0] = socket_vector[1] = -1;

  listener = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (listener == -1)
    return -1;

  if (setup_socketpair(listener, socket_vector) == 0) {
    return 0;
  }

  saved_errno = errno;
  close(listener);
  close(socket_vector[0]);
  close(socket_vector[1]);
  errno = saved_errno;
  socket_vector[0] = socket_vector[1] = -1;
  return -1;
}
