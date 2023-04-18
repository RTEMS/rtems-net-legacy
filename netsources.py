#
# RTEMS Project (https://www.rtems.org/)
#
# Copyright (c) 2023 Chris Johns <chrisj@rtems.org>.
# All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class source:
    network = [
        # rtems
        'rtems/mkrootfs.c',
        'rtems/rtems-bsd-iface.c',
        'rtems/rtems-kernel-program.c',
        'rtems/rtems_bootp.c',
        'rtems/rtems_bsdnet_malloc_starvation.c',
        'rtems/rtems_dhcp.c',
        'rtems/rtems_dhcp_failsafe.c',
        'rtems/rtems_glue.c',
        'rtems/rtems_malloc_mbuf.c',
        'rtems/rtems_mii_ioctl.c',
        'rtems/rtems_mii_ioctl_kern.c',
        'rtems/rtems_select.c',
        'rtems/rtems_showicmpstat.c',
        'rtems/rtems_showifstat.c',
        'rtems/rtems_showipstat.c',
        'rtems/rtems_showmbuf.c',
        'rtems/rtems_showroute.c',
        'rtems/rtems_showtcpstat.c',
        'rtems/rtems_showudpstat.c',
        'rtems/rtems_socketpair.c',
        'rtems/rtems_syscall.c',
        'rtems/rtems_syscall_api.c',
        'rtems/sghostname.c',
        # kernel
        'kern/kern_mib.c',
        'kern/kern_subr.c',
        'kern/kern_sysctl.c',
        'kern/uipc_domain.c',
        'kern/uipc_mbuf.c',
        'kern/uipc_socket.c',
        'kern/uipc_socket2.c',
        # bsps
        'bsps/shared/net/cs8900.c',
        'bsps/shared/net/dec21140.c',
        'bsps/shared/net/elnk.c',
        'bsps/shared/net/greth2.c',
        'bsps/shared/net/i82586.c',
        'bsps/shared/net/if_dc.c',
        'bsps/shared/net/if_fxp.c',
        'bsps/shared/net/open_eth.c',
        'bsps/shared/net/smc91111.c',
        'bsps/shared/net/sonic.c',
        # net
        'net/if.c',
        'net/if_ethersubr.c',
        'net/if_loop.c',
        'net/if_nametoindex.c',
        'net/if_ppp.c',
        'net/ppp_tty.c',
        'net/radix.c',
        'net/raw_cb.c',
        'net/raw_usrreq.c',
        'net/route.c',
        'net/rtsock.c',
        'net/slcompress.c',
        # netinet
        'netinet/if_ether.c',
        'netinet/igmp.c',
        'netinet/in.c',
        'netinet/in_cksum.c',
        'netinet/in_pcb.c',
        'netinet/in_proto.c',
        'netinet/in_rmx.c',
        'netinet/ip_divert.c',
        'netinet/ip_fw.c',
        'netinet/ip_icmp.c',
        'netinet/ip_input.c',
        'netinet/ip_mroute.c',
        'netinet/ip_output.c',
        'netinet/raw_ip.c',
        'netinet/tcp_debug.c',
        'netinet/tcp_input.c',
        'netinet/tcp_output.c',
        'netinet/tcp_subr.c',
        'netinet/tcp_timer.c',
        'netinet/tcp_usrreq.c',
        'netinet/udp_usrreq.c',
        # nfs
        'nfs/bootp_subr.c',
        # rpc
        'librpc/src/rpc/auth_none.c',
        'librpc/src/rpc/auth_unix.c',
        'librpc/src/rpc/authunix_prot.c',
        'librpc/src/rpc/bindresvport.c',
        'librpc/src/rpc/clnt_generic.c',
        'librpc/src/rpc/clnt_perror.c',
        'librpc/src/rpc/clnt_raw.c',
        'librpc/src/rpc/clnt_simple.c',
        'librpc/src/rpc/clnt_tcp.c',
        'librpc/src/rpc/clnt_udp.c',
        'librpc/src/rpc/get_myaddress.c',
        'librpc/src/rpc/getrpcent.c',
        'librpc/src/rpc/getrpcport.c',
        'librpc/src/rpc/netname.c',
        'librpc/src/rpc/netnamer.c',
        'librpc/src/rpc/pmap_clnt.c',
        'librpc/src/rpc/pmap_getmaps.c',
        'librpc/src/rpc/pmap_getport.c',
        'librpc/src/rpc/pmap_prot.c',
        'librpc/src/rpc/pmap_prot2.c',
        'librpc/src/rpc/pmap_rmt.c',
        'librpc/src/rpc/rpc_callmsg.c',
        'librpc/src/rpc/rpc_commondata.c',
        'librpc/src/rpc/rpc_dtablesize.c',
        'librpc/src/rpc/rpc_prot.c',
        'librpc/src/rpc/rpcdname.c',
        'librpc/src/rpc/rtems_portmapper.c',
        'librpc/src/rpc/rtems_rpc.c',
        'librpc/src/rpc/rtime.c',
        'librpc/src/rpc/svc.c',
        'librpc/src/rpc/svc_auth.c',
        'librpc/src/rpc/svc_auth_unix.c',
        'librpc/src/rpc/svc_raw.c',
        'librpc/src/rpc/svc_run.c',
        'librpc/src/rpc/svc_simple.c',
        'librpc/src/rpc/svc_tcp.c',
        'librpc/src/rpc/svc_udp.c',
        'librpc/src/xdr/xdr.c',
        'librpc/src/xdr/xdr_array.c',
        'librpc/src/xdr/xdr_float.c',
        'librpc/src/xdr/xdr_mem.c',
        'librpc/src/xdr/xdr_rec.c',
        'librpc/src/xdr/xdr_reference.c',
        'librpc/src/xdr/xdr_sizeof.c',
        'librpc/src/xdr/xdr_stdio.c',
        # misc
        'libmisc/dummy-networking.c',
        'libmisc/err.c',
        'libmisc/main_ifconfig.c',
        'libmisc/main_netstats.c',
        'libmisc/main_ping.c',
        'libmisc/main_route.c',
        'libmisc/mon-network.c',
        # lib
        'lib/getprotoby.c',
        'lib/rtems_bsdnet_ntp.c',
        'lib/syslog.c',
        # libc
        'libc/base64.c',
        'libc/gai_strerror.c',
        'libc/getaddrinfo.c',
        'libc/gethostbydns.c',
        'libc/gethostbyht.c',
        'libc/gethostbynis.c',
        'libc/gethostnamadr.c',
        'libc/getifaddrs.c',
        'libc/getnameinfo.c',
        'libc/getnetbydns.c',
        'libc/getnetbyht.c',
        'libc/getnetbynis.c',
        'libc/getnetnamadr.c',
        'libc/getproto.c',
        'libc/getprotoent.c',
        'libc/getprotoname.c',
        'libc/getservbyname.c',
        'libc/getservbyport.c',
        'libc/getservent.c',
        'libc/herror.c',
        'libc/if_indextoname.c',
        'libc/if_nameindex.c',
        'libc/inet_addr.c',
        'libc/inet_lnaof.c',
        'libc/inet_makeaddr.c',
        'libc/inet_netof.c',
        'libc/inet_network.c',
        'libc/inet_ntoa.c',
        'libc/inet_ntop.c',
        'libc/inet_pton.c',
        'libc/linkaddr.c',
        'libc/map_v4v6.c',
        'libc/ns_name.c',
        'libc/ns_netint.c',
        'libc/ns_parse.c',
        'libc/ns_print.c',
        'libc/ns_ttl.c',
        'libc/nsap_addr.c',
        'libc/rcmd.c',
        'libc/recv.c',
        'libc/res_comp.c',
        'libc/res_data.c',
        'libc/res_debug.c',
        'libc/res_init.c',
        'libc/res_mkquery.c',
        'libc/res_mkupdate.c',
        'libc/res_query.c',
        'libc/res_send.c',
        'libc/res_stubs.c',
        'libc/res_update.c',
        'libc/send.c',
        'libc/vars.c',
        # libtest
        'libtest/testbeginend.c',
        'libtest/testbusy.c',
        'libtest/testextension.c',
        'libtest/testparallel.c',
        'libtest/testrun.c',
        'libtest/testwrappers.c',
    ]

    nfsclient = [
        'nfsclient/proto/mount_prot_xdr.c',
        'nfsclient/proto/nfs_prot_xdr.c',
        'nfsclient/src/nfs.c',
        'nfsclient/src/rpcio.c',
        'nfsclient/src/sock_mbuf.c',
        'nfsclient/src/xdr_mbuf.c',
    ]

    pppd = [
        'pppd/auth.c',
        'pppd/ccp.c',
        'pppd/chap.c',
        'pppd/chap_ms.c',
        'pppd/chat.c',
        'pppd/demand.c',
        'pppd/fsm.c',
        'pppd/ipcp.c',
        'pppd/lcp.c',
        'pppd/magic.c',
        'pppd/options.c',
        'pppd/rtemsmain.c',
        'pppd/rtemspppd.c',
        'pppd/sys-rtems.c',
        'pppd/upap.c',
        'pppd/utils.c',
    ]


header = {
    '.': ['ifaddrs.h', 'librtemsNfs.h', 'loop.h', 'resolv.h'],
    'arpa': ['arpa/nameser.h', 'arpa/nameser_compat.h'],
    'dev/mii': ['dev/mii/mii.h'],
    'libchip': [
        'bsps/include/libchip/cs8900.h',
        'bsps/include/libchip/greth.h',
        'bsps/include/libchip/i82586var.h',
        'bsps/include/libchip/if_dcreg.h',
        'bsps/include/libchip/if_fxpvar.h',
        'bsps/include/libchip/open_eth.h',
        'bsps/include/libchip/smc91111.h',
        'bsps/include/libchip/smc91111exp.h',
        'bsps/include/libchip/sonic.h',
    ],
    'machine': [
        'machine/_align.h', 'machine/_kernel_if.h', 'machine/_kernel_lock.h',
        'machine/_kernel_socket.h', 'machine/cpu.h', 'machine/cpufunc.h',
        'machine/in_cksum.h', 'machine/limits.h', 'machine/vmparam.h'
    ],
    'net': [
        'net/bpf.h', 'net/ethernet.h', 'net/if_arp.h', 'net/if_dl.h',
        'net/if_llc.h', 'net/if_media.h', 'net/if_ppp.h', 'net/if_pppvar.h',
        'net/if_types.h', 'net/if_var.h', 'net/netisr.h', 'net/ppp_comp.h',
        'net/ppp_defs.h', 'net/radix.h', 'net/raw_cb.h', 'net/route.h',
        'net/slcompress.h'
    ],
    'netinet': [
        'netinet/icmp_var.h', 'netinet/if_ether.h', 'netinet/igmp.h',
        'netinet/igmp_var.h', 'netinet/in_pcb.h', 'netinet/in_systm.h',
        'netinet/in_var.h', 'netinet/ip.h', 'netinet/ip_fw.h',
        'netinet/ip_icmp.h', 'netinet/ip_mroute.h', 'netinet/ip_var.h',
        'netinet/tcp_debug.h', 'netinet/tcp_fsm.h', 'netinet/tcp_seq.h',
        'netinet/tcp_timer.h', 'netinet/tcp_var.h', 'netinet/tcpip.h',
        'netinet/udp.h', 'netinet/udp_var.h'
    ],
    'nfs': ['nfs/nfsproto.h', 'nfs/rpcv2.h', 'nfs/xdr_subs.h'],
    'nfsclient': [
        'nfsclient/nfsargs.h',
        'nfsclient/nfsdiskless.h',
    ],
    'rpc': [
        'rpc/auth.h', 'rpc/auth_unix.h', 'rpc/clnt.h', 'rpc/clnt_soc.h',
        'rpc/clnt_stat.h', 'rpc/pmap_clnt.h', 'rpc/pmap_prot.h',
        'rpc/pmap_rmt.h', 'rpc/rpc.h', 'rpc/rpc_com.h', 'rpc/rpc_msg.h',
        'rpc/rpcent.h', 'rpc/svc.h', 'rpc/svc_auth.h', 'rpc/svc_soc.h',
        'rpc/types.h', 'rpc/xdr.h'
    ],
    'rtems': [
        'include/rtems/rtemspppd.h', 'rtems/bootp.h', 'rtems/dhcp.h',
        'rtems/mkrootfs.h', 'rtems/rtems_bsdnet.h',
        'rtems/rtems_bsdnet_internal.h', 'rtems/rtems_dhcp_failsafe.h',
        'rtems/rtems_mii_ioctl.h', 'rtems/rtems_netdb.h',
        'rtems/rtems_netinet_in.h', 'rtems/rtems_syscall.h'
    ],
    'rtems/bsd': [
        'include/rtems/bsd/iface.h',
    ],
    'rtems/bsdnet': ['rtems/bsdnet/_types.h', 'rtems/bsdnet/servers.h'],
    'sys': [
        'sys/callout.h', 'sys/conf.h', 'sys/domain.h', 'sys/kernel.h',
        'sys/libkern.h', 'sys/linker_set.h', 'sys/malloc.h', 'sys/mbuf.h',
        'sys/mount.h', 'sys/proc.h', 'sys/protosw.h', 'sys/reboot.h',
        'sys/resourcevar.h', 'sys/selinfo.h', 'sys/signalvar.h',
        'sys/socketvar.h', 'sys/sysctl.h', 'sys/systm.h', 'sys/ucred.h'
    ],
    'vm': ['vm/vm.h', 'vm/vm_extern.h', 'vm/vm_kern.h', 'vm/vm_param.h'],
}
