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

from __future__ import print_function
from rtems_waf import rtems

import netlegacy
import sys

top = '.'

rtems_version = "6"
subdirs = ['testsuites']

try:
    import rtems_waf.rtems as rtems
except rtems_waf.DoesNotExist:
    print("error: no rtems_waf git submodule; see README.waf")
    sys.exit(1)


def init(ctx):
    rtems.init(ctx, version=rtems_version, long_commands=True)


def options(opt):
    rtems.options(opt)
    netlegacy.options(opt)
    copts = opt.option_groups['configure options']
    copts.add_option('--net-test-config',
                     default='config.inc',
                     dest='net_config',
                     help='Network test configuration (default: %default)')


def bsp_configure(conf, arch_bsp):
    env = conf.env.derive()
    ab = conf.env.RTEMS_ARCH_BSP
    conf.msg('Configure variant: ', ab)
    conf.setenv(ab, env)
    netlegacy.bsp_configure(conf, arch_bsp)
    conf.setenv(ab)


def configure(conf):
    conf.env.NET_CONFIG = conf.options.net_config
    rtems.configure(conf, bsp_configure)


def recurse(ctx):
    for sd in subdirs:
        ctx.recurse(sd)


def build(bld):
    rtems.build(bld)
    netlegacy.build(bld)
    bld.add_group()
    recurse(bld)
