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


def options(opt):
    pass


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
    conf.env.IFLAGS = [str(conf.path.find_node(i))
                       for i in includes] + conf.env.IFLAGS
    conf.env.OPTIMIZATION = ['-O2']


def build(bld):
    arch_bsp = bld.env.RTEMS_ARCH_BSP
    ab = rtems.arch(arch_bsp) + '/' + rtems.bsp(arch_bsp)

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
                      ["libnetworking.a", 'libpppd.a', 'libnfs.a'])
    for inc_dir in netsources.header:
        for header in netsources.header[inc_dir]:
            hname = os.path.basename(header)
            bld.install_as(
                os.path.join(bld.env.PREFIX, arch_inc_path, inc_dir, hname),
                header)
