#
# RTEMS Project (https://www.rtems.org/)
#
# Copyright (c) 2021 Regents of University of Colorado
# Written by Vijay Kumar Banerjee <vijay@rtems.org>.
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

import os
import os.path

from rtems_waf import rtems

import bsp_drivers
import netsources


def net_config_header(bld):
    if not os.path.exists(bld.env.NET_CONFIG):
        bld.fatal('network configuraiton \'%s\' not found' %
                  (bld.env.NET_CONFIG))
    net_tags = [
        'NET_CFG_IFACE', 'NET_CFG_BOOT_PROT', 'NET_CFG_SELF_IP',
        'NET_CFG_NETMASK', 'NET_CFG_MAC_ADDR', 'NET_CFG_GATEWAY_IP'
    ]
    try:
        net_cfg_lines = open(bld.env.NET_CONFIG).readlines()
    except:
        bld.fatal('network configuraiton \'%s\' read failed' %
                  (bld.env.NET_CONFIG))
    lc = 0
    sed = 'sed '
    net_defaults = {}
    for l in net_cfg_lines:
        lc += 1
        if not l.strip().startswith('NET_CFG_'):
            bld.fatal('network configuration \'%s\' ' \
                      'invalid config: %d: %s' % (bld.env.NET_CONFIG, lc, l))
        ls = l.split('=')
        if len(ls) != 2:
            bld.fatal('network configuration \'%s\' ' \
                      'parse error: %d: %s' % (bld.env.NET_CONFIG, lc, l))
        lhs = ls[0].strip()
        rhs = ls[1].strip()
        if lhs in net_tags:
            net_defaults[lhs] = rhs
        else:
            bld.fatal('network configuration \'%s\' ' \
                      'invalid config: %d: %s' % (bld.env.NET_CONFIG, lc, l))
    for cfg in net_defaults:
        sed += "-e 's/@%s@/%s/' " % (cfg, net_defaults[cfg])
    bld(target=bld.env.NETWORK_CONFIG,
        source='testsuites/include/network-config.h.in',
        rule=sed + ' < ${SRC} > ${TGT}',
        update_outputs=True)


def options(opt):
    copts = opt.option_groups['configure options']
    copts.add_option('--net-test-config',
                     default='config.inc',
                     dest='net_config',
                     help='Network test configuration (default: %default)')
    copts.add_option('--optimization',
                     default='-O2',
                     dest='optimization',
                     help='Optimaization level (default: %default)')


def bsp_configure(conf, arch_bsp, mandatory=True):
    ab = rtems.arch(arch_bsp) + '/' + rtems.bsp(arch_bsp)
    includes = [
        '.',
        'include',
        'bsps/include',
        'testsuites/include',
    ]
    if ab in bsp_drivers.include:
        includes += bsp_drivers.include[ab]
    bld_inc = conf.path.get_bld().find_or_declare('include')
    conf.env.NETWORK_CONFIG = str(bld_inc.find_or_declare('network-config.h'))
    conf.env.IFLAGS = [str(bld_inc)
                       ] + [str(conf.path.find_node(i))
                            for i in includes] + conf.env.IFLAGS
    conf.env.OPTIMIZATION = [conf.options.optimization]
    #
    # BSPs must define:
    #  - RTEMS_BSP_NETWORK_DRIVER_NAME
    #  - RTEMS_BSP_NETWORK_DRIVER_ATTACH
    #
    for define in [
            'RTEMS_BSP_NETWORK_DRIVER_NAME', 'RTEMS_BSP_NETWORK_DRIVER_ATTACH'
    ]:
        code = ['#include <bspopts.h>']
        code += ['#include <bsp.h>']
        code += ['#ifndef %s' % (define)]
        code += ['  #error %s not defined' % (define)]
        code += ['#endif']
        try:
            conf.check_cc(fragment=rtems.test_application(code),
                          execute=False,
                          msg='Checking for %s' % (define))
        except conf.errors.WafError:
            conf.fatal(ab + ' does not provide %s' % (define))


def build(bld):
    arch_bsp = bld.env.RTEMS_ARCH_BSP
    ab = rtems.arch(arch_bsp) + '/' + rtems.bsp(arch_bsp)

    net_config_header(bld)

    if ab in bsp_drivers.source:
        bld(target='bspobjs',
            features='c',
            cflags=bld.env.OPTIMIZATION + ['-g'],
            includes=bld.env.IFLAGS,
            source=bsp_drivers.source[ab])

    bld(target='netobjs',
        features='c',
        cflags=bld.env.OPTIMIZATION + ['-g'],
        includes=bld.env.IFLAGS,
        defines=['IN_HISTORICAL_NETS=1'],
        source=netsources.source.network)

    bld(target='networking', features='c cstlib', use=['bspobjs', 'netobjs'])

    bld.stlib(target='pppd',
              features='c',
              cflags=bld.env.OPTIMIZATION + ['-g'],
              includes=bld.env.IFLAGS,
              use=['networking'],
              source=netsources.source.pppd)

    bld.stlib(target='nfs',
              features='c',
              cflags=bld.env.OPTIMIZATION + ['-g'],
              includes=bld.env.IFLAGS,
              use=['networking'],
              source=netsources.source.nfsclient)

    arch_lib_path = rtems.arch_bsp_lib_path(bld.env.RTEMS_VERSION,
                                            bld.env.RTEMS_ARCH_BSP)
    arch_inc_path = rtems.arch_bsp_include_path(bld.env.RTEMS_VERSION,
                                                bld.env.RTEMS_ARCH_BSP)

    bld.install_files(os.path.join(bld.env.PREFIX, arch_lib_path),
                      ['libnetworking.a', 'libpppd.a', 'libnfs.a'])
    for inc_dir in netsources.header:
        for header in netsources.header[inc_dir]:
            hname = os.path.basename(header)
            bld.install_as(
                os.path.join(bld.env.PREFIX, arch_inc_path, inc_dir, hname),
                header)
