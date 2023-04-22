/*
 * Copyright (c) 2018 embedded brains GmbH.  All rights reserved.
 *
 *  embedded brains GmbH
 *  Dornierstr. 4
 *  82178 Puchheim
 *  Germany
 *  <rtems@embedded-brains.de>
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
#include <string.h>

#include <rtems.h>
#include <rtems/dhcp.h>
#include <rtems/rtems_bsdnet.h>
#include <rtems/telnetd.h>

#include <tmacros.h>
#include <net-legacy-config.h>
#include <network-config.h>

const char rtems_test_name[] = "TELNETD 2";

struct rtems_bsdnet_config rtems_bsdnet_config;

rtems_shell_env_t env;

static void telnet_shell( char *name, void *arg )
{
  rtems_shell_dup_current_env( &env );

  env.devname = name;
  env.taskname = "TLNT";

  rtems_shell_main_loop( &env );
}

rtems_telnetd_config_table rtems_telnetd_config = {
  .command = telnet_shell,
  .stack_size = 8 * RTEMS_MINIMUM_STACK_SIZE,
};

static rtems_task Init(rtems_task_argument argument)
{
  rtems_status_code sc;
  int rv;

  TEST_BEGIN();

  rtems_test_assert(rtems_net_legacy_config(&rtems_bsdnet_config));

  rv = rtems_bsdnet_initialize_network();
  rtems_test_assert(rv == 0);

  sc = rtems_telnetd_start( &rtems_telnetd_config );
  rtems_test_assert( sc == RTEMS_SUCCESSFUL );

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

  TEST_END();
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

extern rtems_shell_cmd_t rtems_shell_SYSCTL_Command;
#define CONFIGURE_SHELL_USER_COMMANDS \
  &rtems_shell_SYSCTL_Command

#include <rtems/shellconfig.h>

#include <rtems/confdefs.h>
