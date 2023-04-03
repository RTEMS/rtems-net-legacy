/*
 * Copyright (c) 2023 Chris Johns.  All rights reserved.
 *
 * The license and distribution terms for this file may be
 * found in the file LICENSE in this distribution or at
 * http://www.rtems.org/license/LICENSE.
 */

#ifndef _NET_LEGACY_CONFIG_H
#define _NET_LEGACY_CONFIG_H

#include <stdbool.h>

struct rtems_bsdnet_config;

bool rtems_net_legacy_config(struct rtems_bsdnet_config* bsd);

#endif
