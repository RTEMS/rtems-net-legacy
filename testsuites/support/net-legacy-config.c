/*
 * Copyright (c) 2023 Chris Johns.  All rights reserved.
 *
 * The license and distribution terms for this file may be
 * found in the file LICENSE in this distribution or at
 * http://www.rtems.org/license/LICENSE.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdio.h>

#include <bsp.h>
#include <rtems.h>
#include <rtems/dhcp.h>
#include <rtems/rtems_bsdnet.h>

#include <net-legacy-config.h>
#include <network-config.h>

static char* iface = NET_CFG_IFACE;
static char* boot_prot = NET_CFG_BOOT_PROT;
static char* ip = NET_CFG_SELF_IP;
static char* netmask = NET_CFG_NETMASK;
static char* gateway = NET_CFG_GATEWAY_IP;
static char* domainname = NET_CFG_DOMAINNAME;
static char* dns_ip = NET_CFG_DNS_IP;
static char* ntp = NET_CFG_NTP_IP;
static struct rtems_bsdnet_ifconfig ifcfg = {
  RTEMS_BSP_NETWORK_DRIVER_NAME,
  RTEMS_BSP_NETWORK_DRIVER_ATTACH
};

bool rtems_net_legacy_config(struct rtems_bsdnet_config* bsd) {
  if (bsd->ifconfig == NULL) {
    bsd->ifconfig = &ifcfg;
  }
  ifcfg.name = iface;
  ifcfg.ip_address = ip;
  ifcfg.ip_netmask = netmask;
  bsd->gateway = gateway;
  bsd->domainname = domainname;
  bsd->name_server[0] = dns_ip;
  bsd->ntp_server[0] = ntp;
  if (strcmp(boot_prot, "static") == 0) {
    bsd->bootp = NULL;
  } else if (strcmp(boot_prot, "bootp") == 0) {
    bsd->bootp = rtems_bsdnet_do_bootp;
  } else if (strcmp(boot_prot, "dhcp") == 0) {
    bsd->bootp = rtems_bsdnet_do_dhcp;
  } else {
    printf("%s: %d: invalid network configuration: %s\n",
           __FILE__, __LINE__, boot_prot);
    return false;
  }
  return true;
}
