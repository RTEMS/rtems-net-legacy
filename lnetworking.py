#
# RTEMS Project (https://www.rtems.org/)
#
# Copyright (c) 2021 Vijay Kumar Banerjee <vijaykumar9597@gmail.com>.
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

from rtems_waf import rtems
import bsp_drivers
import os

source_files = []
include_files = {}
test_source = []
exclude_dirs = ['pppd', 'nfsclient', 'testsuites', 'librpc/include', 'bsps']
exclude_headers = ['rtems-bsd-user-space.h', 'rtems-bsd-kernel-space.h']

for root, dirs, files in os.walk("."):
    [dirs.remove(d) for d in list(dirs) if d in exclude_dirs]
    include_files[root[2:]] = []
    for name in files:
        if name[-2:] == '.c':
            source_files.append(os.path.join(root, name))
        if name[-2:] == '.h' and name not in exclude_headers:
            include_files[root[2:]].append(os.path.join(root,name))

for root, dirs, files in os.walk('./testsuites'):
    for name in files:
        if name [-2:] == '.c':
            test_source.append(os.path.join(root, name))

def build(bld):
    include_path = []
    ip = ''
    BSP = bld.env.RTEMS_ARCH_BSP.split('-')[-1]

    bsp_dirs, bsp_sources, bsp_archs = bsp_drivers.bsp_files(bld)

    include_path.extend(['.',
                         os.path.relpath(bld.env.PREFIX),
                         './testsuites/include',
                         os.path.relpath(os.path.join(bld.env.PREFIX, 'include')),
                         './bsps/include'])
    arch_lib_path = rtems.arch_bsp_lib_path(bld.env.RTEMS_VERSION,
                                            bld.env.RTEMS_ARCH_BSP)
    include_path.append(os.path.relpath(os.path.join(bld.env.PREFIX,
                                                     arch_lib_path)))
    include_path.append(os.path.relpath(os.path.join(bld.env.PREFIX,
                                                     arch_lib_path,
                                                     'include')))
    if BSP in bsp_dirs:
        include_path.extend(bsp_dirs[BSP])

    for i in include_path:
        ip = ip + i + ' '

    if (BSP in bsp_sources):
        bld(target = 'bsp_objs',
            features = 'c',
            cflags = ['-O2', '-g'],
            includes = ip,
            source = bsp_sources[BSP])

    bld(target = 'network_objects',
        features = 'c',
        includes = ip,
        source = source_files)

    bld(target = 'networking',
        features = 'c cstlib',
        use = ['bsp_objs', 'network_objects'])

    bld.program(target = 'networking01.exe',
                features = 'c cprogram',
                cflags = ['-O2', '-g'],
                includes = ip,
                use = 'networking',
                source = test_source)

    bld.install_files(os.path.join('${PREFIX}', arch_lib_path), ["libnetworking.a"])
    for i in include_files:
        bld.install_files(os.path.join('${PREFIX}', arch_lib_path, i), include_files[i])
