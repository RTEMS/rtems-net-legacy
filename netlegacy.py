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

from rtems_waf import rtems
import bsp_drivers
import os

source_files = []
include_files = {}
exclude_dirs = ['pppd', 'nfsclient', 'testsuites', os.path.join('librpc', 'include'), 'bsps']
exclude_headers = ['rtems-bsd-user-space.h', 'rtems-bsd-kernel-space.h']

for root, dirs, files in os.walk("."):
    [dirs.remove(d) for d in list(dirs) if d in exclude_dirs]
    dirs.append(os.path.join('bsps', 'shared', 'net'))
    include_files[root[2:]] = []
    for name in files:
        ext = os.path.splitext(name)[1]
        if ext == '.c':
            source_files.append(os.path.join(root, name))
        if ext == '.h' and name not in exclude_headers:
            include_files[root[2:]].append(os.path.join(root, name))


def find_node(bld, *paths):
    path = os.path.join(*paths)
    return os.path.relpath(str(bld.path.find_node(path)))


def install_file_list(*paths):
    path = os.path.join(*paths)
    file_list = [os.path.join(path, f) for f in os.listdir(path)]
    return file_list

def options(opt):
    pass


def bsp_configure(conf, arch_bsp, mandatory = True):
    pass


def build(bld):
    include_path = []
    ip = ''
    bsp = bld.env.RTEMS_ARCH_BSP.split('-')[-1]
    pppd_source = [os.path.join('pppd', s)
                   for s in os.listdir('pppd')
                   if os.path.splitext(s)[1] == '.c']
    nfs_source = []
    for root, dirs, files in os.walk('nfsclient'):
        for name in files:
            ext = os.path.splitext(name)[1]
            if ext == '.c':
                src_root = os.path.split(root)
                nfs_source.append(os.path.join(src_root[0], src_root[1], name))

    bsp_dirs, bsp_sources = bsp_drivers.bsp_files(bld)

    include_path.extend(['.',
                         'include',
                         os.path.relpath(bld.env.PREFIX),
                         os.path.join('testsuites', 'include'),
                         os.path.relpath(os.path.join(bld.env.PREFIX,
                                                      'include')),
                         os.path.join('bsps', 'include')])
    arch_lib_path = rtems.arch_bsp_lib_path(bld.env.RTEMS_VERSION,
                                            bld.env.RTEMS_ARCH_BSP)
    lib_path = os.path.join(bld.env.PREFIX, arch_lib_path)
    include_path.append(os.path.relpath(os.path.join(bld.env.PREFIX,
                                                     arch_lib_path)))
    include_path.append(os.path.relpath(os.path.join(bld.env.PREFIX,
                                                     arch_lib_path,
                                                     'include')))
    include_path.append(find_node(bld, 'bsps', 'include', 'libchip'))

    bld.read_stlib('rtemsbsp', paths=[lib_path])

    if bsp in bsp_dirs:
        include_path.extend(bsp_dirs[bsp])

    for i in include_path:
        ip = ip + i + ' '

    if (bsp in bsp_sources):
        bld(target='bsp_objs',
            features='c',
            cflags=['-O2', '-g'],
            includes=ip,
            source=bsp_sources[bsp])

    bld(target='network_objects',
        features='c',
        includes=ip,
        defines=['IN_HISTORICAL_NETS=1'],
        source=source_files)

    bld(target='networking',
        features='c cstlib',
        use=['bsp_objs', 'network_objects'])

    bld.stlib(target='pppd',
              features='c',
              includes=ip,
              use='networking',
              source=pppd_source)

    bld.stlib(target='nfs',
              features='c',
              includes=ip,
              use=['rtemsbsp', 'networking'],
              source=nfs_source)

    bld.install_files(os.path.join(bld.env.PREFIX, arch_lib_path),
                      ["libnetworking.a", 'libpppd.a', 'libnfs.a'])
    bld.install_files(os.path.join(bld.env.PREFIX, arch_lib_path,
                                   'include', 'libchip'),
                      install_file_list('bsps', 'include', 'libchip'))
    for i in include_files:
        if 'include' in os.path.split(i):
            bld.install_files(os.path.join(bld.env.PREFIX,
                                           arch_lib_path, i),
                              include_files[i])
        else:
            bld.install_files(os.path.join(bld.env.PREFIX,
                                           arch_lib_path, 'include', i),
                              include_files[i])
