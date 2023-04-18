/*
 * Copyright (c) 2023 Chris Johns <chris@contemporay.software>.  All rights reserved.
 *
 * The license and distribution terms for this file may be
 * found in the file LICENSE in this distribution or at
 * http://www.rtems.org/license/LICENSE.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <rtems.h>
#include <rtems/dhcp.h>
#include <rtems/rtems_bsdnet.h>
#include <rtems/telnetd.h>

#include <tmacros.h>
#include <net-legacy-config.h>
#include <network-config.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <resolv.h>

#define START_SHELL 0

const char rtems_test_name[] = "RESOLVE";

#define MACH_SIZE 45
static const char* mach[MACH_SIZE] = {
  "localhost",
  "anoncvs.cirr.com",
  "anoncvs.netbsd.se",
  "antioche.antioche.eu.org",
  "centaurus.4web.cz",
  "chur.math.ntnu.no",
  "console.netbsd.org",
  "cvs.netbsd.org",
  "cvsup.netbsd.se",
  "ftp.chg.ru",
  "ftp.estpak.ee",
  "ftp.fsn.hu",
  "ftp.funet.fi",
  "ftp.netbsd.org",
  "ftp.nluug.nl",
  "ftp.plig.org",
  "ftp.uni-erlangen.de",
  "ftp.xgate.co.kr",
  "gd.tuwien.ac.at",
  "gort.ludd.luth.se",
  "irc.warped.net",
  "knug.youn.co.kr",
  "mail.jp.netbsd.org",
  "mail.netbsd.org",
  "melanoma.cs.rmit.edu.au",
  "mirror.aarnet.edu.au",
  "moon.vub.ac.be",
  "net.bsd.cz",
  "netbsd.3miasto.net",
  "netbsd.4ka.mipt.ru",
  "netbsd.csie.nctu.edu.tw",
  "netbsd.enderunix.org",
  "netbsd.ftp.fu-berlin.de",
  "netbsd.pair.com",
  "netbsdiso.interoute.net.uk",
  "netbsdwww.cs.rmit.edu.au",
  "netbsdwww.interoute.net.uk",
  "ns.netbsd.org",
  "skeleton.phys.spbu.ru",
  "www.en.netbsd.de",
  "www.netbsd.cl",
  "www.netbsd.nl",
  "www.netbsd.org",
  "www.netbsd.ro",
  "zeppo.rediris.es"
};

extern int addrinfo_read_hostlist_func(struct addrinfo *ai, const char *line);

static int resolve_test(void) {
  struct addrinfo addr;
  size_t l;
  int r = 0;
  printf("getaddrinfo test start\n");
  for (l = 0; l < MACH_SIZE - 1; ++l) {
    r = addrinfo_read_hostlist_func(&addr, mach[l]);
    if (r != 0) {
      break;
    }
  }
  fflush(stdout);
  printf("getaddrinfo test finish\n\n\n");
  sleep(2);
  return r;
}

struct rtems_bsdnet_config rtems_bsdnet_config;

static rtems_task Init(rtems_task_argument argument)
{
  rtems_status_code sc;
  int rv;

  TEST_BEGIN();

  rtems_test_assert(rtems_net_legacy_config(&rtems_bsdnet_config));

  rtems_bsdnet_config.domainname = "gemini.edu";
  rtems_bsdnet_config.name_server[0] = "10.1.5.8";

  rv = rtems_bsdnet_initialize_network();
  rtems_test_assert(rv == 0);

  rv = resolve_test();
  rtems_test_assert(rv == 0);

#if START_SHELL
  sc = rtems_shell_init(
    "SHLL",                       /* task name */
    RTEMS_MINIMUM_STACK_SIZE * 4, /* task stack size */
    1,                            /* task priority */
    "/dev/console",               /* device name */
    false,                        /* run forever */
    true,                         /* wait for shell to terminate */
    NULL                          /* login check function,
                                     use NULL to disable a login check */
  );
  rtems_test_assert( sc == RTEMS_SUCCESSFUL );
#endif

  TEST_END();
  sleep(2);
  rtems_test_exit(0);
}

#define CONFIGURE_INIT

#define CONFIGURE_MICROSECONDS_PER_TICK 10000

#define CONFIGURE_APPLICATION_NEEDS_CLOCK_DRIVER
#define CONFIGURE_APPLICATION_NEEDS_CONSOLE_DRIVER
#define CONFIGURE_APPLICATION_NEEDS_LIBBLOCK

#define CONFIGURE_MAXIMUM_FILE_DESCRIPTORS 32

#define CONFIGURE_MAXIMUM_TASKS 12

#define CONFIGURE_MAXIMUM_POSIX_KEYS 10
#define CONFIGURE_MAXIMUM_SEMAPHORES 20
#define CONFIGURE_MAXIMUM_MESSAGE_QUEUES 10

#define CONFIGURE_INITIAL_EXTENSIONS RTEMS_TEST_INITIAL_EXTENSION

#define CONFIGURE_RTEMS_INIT_TASKS_TABLE

#define CONFIGURE_INIT_TASK_ATTRIBUTES RTEMS_FLOATING_POINT

#define CONFIGURE_UNLIMITED_OBJECTS
#define CONFIGURE_UNIFIED_WORK_AREAS

#define RTEMS_NETWORKING 1
#define CONFIGURE_SHELL_COMMANDS_INIT
#define CONFIGURE_SHELL_COMMANDS_ALL
#define CONFIGURE_SHELL_COMMANDS_ALL_NETWORKING

#include <rtems/shellconfig.h>

#include <rtems/confdefs.h>
