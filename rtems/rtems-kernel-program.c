/*
 * Copyright (C) 2022 On-Line Applications Research Corporation (OAR)
 * Written by Kinsey Moore <kinsey.moore@oarcorp.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <machine/rtems-bsd-kernel-space.h>
#include <machine/rtems-bsd-thread.h>

#include <sys/types.h>
#include <sys/kernel.h>

#include <stdio.h>

#include <rtems/extension.h>
#include <rtems/score/percpu.h>
#include <rtems/score/thread.h>
#include <rtems/sysinit.h>

static size_t rtems_bsd_extension_index;

static const rtems_extensions_table rtems_bsd_extensions = {};

/*
 * This must only be run after the system has become multithreading such as in
 * Init(). This must not be run as part of normal RTEMS initialization as part
 * of a SYSINIT call.
 */
void rtems_bsd_compat_initialize(void)
{
  rtems_id ext_id;
  rtems_status_code sc;

  sc = rtems_extension_create(
    BSD_TASK_NAME,
    &rtems_bsd_extensions,
    &ext_id
  );
  if (sc != RTEMS_SUCCESSFUL) {
    printf("%s: cannot create extension\n",  __func__);
    rtems_task_suspend(RTEMS_SELF);
    rtems_fatal_error_occurred(0xdeadbeef);
  }

  rtems_bsd_extension_index = rtems_object_id_get_index(ext_id);
}

static struct rtems_bsd_program_control **
rtems_bsd_get_bsd_extension_ptr(void)
{
  Thread_Control *executing = _Thread_Get_executing();
  return ( struct rtems_bsd_program_control ** )&executing->extensions[rtems_bsd_extension_index];
}

struct rtems_bsd_program_control *
rtems_bsd_program_get_control_or_null(void)
{
  return *rtems_bsd_get_bsd_extension_ptr();
}

int
rtems_bsd_program_set_control(struct rtems_bsd_program_control *prog_ctrl)
{
  *rtems_bsd_get_bsd_extension_ptr() = prog_ctrl;
  return 0;
}
