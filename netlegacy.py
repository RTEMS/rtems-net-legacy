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

from rtems_waf import git
from rtems_waf import rtems
from rtems_waf import version

import bsp_drivers
import netsources


def version_header(bld):
    if isinstance(bld.env.RTEMS_NET_LEGACY_REVISION, int):
        revision = bld.env.RTEMS_NET_LEGACY_REVISION
    else:
        revision = '"' + bld.env.RTEMS_NET_LEGACY_REVISION + '"'
    versions = {
        'RTEMS_NET_LEGACY_VERSION':
        '"' + bld.env.RTEMS_NET_LEGACY_VERSION + '"',
        'RTEMS_NET_LEGACY_MAJOR': bld.env.RTEMS_NET_LEGACY_MAJOR,
        'RTEMS_NET_LEGACY_REVISION': revision,
    }
    sed = 'sed '
    for cfg in versions:
        sed += "-e 's/@%s@/%s/' " % (cfg, versions[cfg])
    bld(target='include/machine/rtems-net-legacy.h',
        source='include/machine/rtems-net-legacy.h.in',
        rule=sed + ' < ${SRC} > ${TGT}',
        shell=True)


def options(opt):
    copts = opt.option_groups['configure options']
    copts.add_option('--net-test-config',
                     default='config.inc',
                     dest='net_config',
                     help='Network test configuration (default: %(default)s)')
    copts.add_option('--optimization',
                     default='-O2',
                     dest='optimization',
                     help='Optimization level (default: %(default)s)')
    copts.add_option(
        '--enable-warnings',
        action='store_true',
        dest='warnings',
        help='Enable warnings for all sources (default: %(default)s)')


def bsp_configure(conf, arch_bsp, mandatory=True):
    conf.start_msg('Checking version')
    version.load_rtems_version_header(conf, conf.env.RTEMS_VERSION, arch_bsp,
                                      conf.env.IFLAGS)
    conf.env.RTEMS_NET_LEGACY_VERSION = version.string(conf)
    conf.env.RTEMS_NET_LEGACY_MAJOR = version.version(conf)
    conf.env.RTEMS_NET_LEGACY_REVISION = version.revision(conf)
    conf.end_msg(conf.env.RTEMS_NET_LEGACY_VERSION)
    ab = rtems.arch_bsp_name(arch_bsp)
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
    if conf.options.warnings:
        warnings = '-Wall'
    else:
        warnings = '-w'
    conf.env.WARNINGS = [warnings]
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
    ab = rtems.arch_bsp_name(bld.env.RTEMS_ARCH_BSP)

    version_header(bld)

    bld.add_group()

    cflags = bld.env.OPTIMIZATION + bld.env.WARNINGS + ['-g']

    if ab in bsp_drivers.source:
        bld(target='bspobjs',
            features='c',
            cflags=cflags,
            includes=bld.env.IFLAGS,
            source=bsp_drivers.source[ab])

    bld(target='netobjs',
        features='c',
        cflags=cflags,
        includes=bld.env.IFLAGS,
        defines=['IN_HISTORICAL_NETS=1'],
        source=netsources.source.network)

    bld(target='networking', features='c cstlib', use=['bspobjs', 'netobjs'])

    bld.stlib(target='pppd',
              features='c',
              cflags=cflags,
              includes=bld.env.IFLAGS,
              use=['networking'],
              source=netsources.source.pppd)

    bld.stlib(target='nfs',
              features='c',
              cflags=cflags,
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
    bld.install_as(
        os.path.join(bld.env.PREFIX, arch_inc_path, 'machine',
                     'rtems-net-legacy.h'),
        'include/machine/rtems-net-legacy.h')

    bld.add_group()
