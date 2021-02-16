#
# RTEMS Project (https://www.rtems.org/)
#
# Copyright (c) 2021 Vijay Kumar Banerjee <vijay@rtems.org>.
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
import os
import waflib.Options
import waflib.ConfigSet

def bsp_files(bld):
    source_files = {}
    include_dirs = {}
    bsp_archs = {}
    include_files = []

    bsp_list = bld.env.RTEMS_ARCH_BSP_LIST

    for bl in bsp_list:
        bsp = bl.split('-')[-1]
        arch = bl.split('-')[0]
        bsp_archs[bsp] = bl
        for root, dirs, files in os.walk(os.path.join('./bsps', arch, bsp)):
            include_dirs[bsp] = []
            source_files[bsp] = []
            for name in files:
                if name[-2:] == '.c':
                    source_files[bsp].append(os.path.join(root, name))
                if name[-2:] == '.h':
                    if root not in include_dirs[bsp]:
                        include_dirs[bsp].append(root)
    return (include_dirs, source_files, bsp_archs)
