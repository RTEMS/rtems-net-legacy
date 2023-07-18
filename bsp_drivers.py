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

include = {
    'arm/csb336': [
        'bsps/arm/csb336/net',
    ],
    'arm/csb337': [
        'bsps/arm/csb337/net',
    ],
    'arm/edb7312': [
        'bsps/arm/edb7312/net',
    ],
    'arm/gumstix': [
        'bsps/arm/gumstix/net',
    ],
    'arm/rtl22xx': [
        'bsps/arm/rtl22xx/net',
    ],
    'bfin/bf537Stamp': [
        'bsps/bfin/bf537Stamp/net',
    ],
    'i386/pc386': [
        'bsps/i386/pc386/net',
    ],
    'lm32/lm32_evr': [
        'bsps/lm32/include',
        'bsps/lm32/shared/net',
    ],
    'm68k/av5282': [
        'bsps/m68k/av5282/net',
    ],
    'm68k/csb360': [
        'bsps/m68k/csb360/net',
    ],
    'm68k/mcf5235': [
        'bsps/m68k/mcf5235/net',
    ],
    'm68k/mcf5329': [
        'bsps/m68k/mcf5329/net',
    ],
    'm68k/mvme167': [
        'bsps/m68k/mvme167/net',
    ],
    'm68k/uC5282': [
        'bsps/m68k/uC5282/net',
    ],
    'mips/csb350': [
        'bsps/mips/csb350/net',
    ],
    'powerpc/beatnik': [
        'bsps/powerpc/beatnik/include',
        'bsps/powerpc/beatnik/include/bsp',
        'bsps/powerpc/beatnik/net',
        'bsps/powerpc/beatnik/net/if_em',
        'bsps/powerpc/beatnik/net/if_gfe',
        'bsps/powerpc/beatnik/net/if_mve',
        'bsps/powerpc/beatnik/net/porting',
    ],
    'powerpc/mpc8260ads': [
        'bsps/powerpc/mpc8260ads/net',
    ],
    'powerpc/mvme3100': [
        'bsps/powerpc/mvme3100/net',
    ],
    'powerpc/mvme5500': [
        'bsps/powerpc/mvme5500/net',
    ],
    'powerpc/psim': [
        'bsps/powerpc/psim/net',
    ],
    'powerpc/virtex': [
        'bsps/powerpc/virtex/net',
    ],
    'riscv/griscv': [
        'bsps/riscv/griscv/net',
    ],
    'sparc/erc32': [
        'bsps/sparc/erc32/net',
    ],
    'sparc/leon2': [
        'bsps/sparc/leon2/net',
    ],
    'sparc/leon3': [
        'bsps/sparc/leon3/net',
    ],
}

source = {
    'arm/atsamv': [
        'bsps/arm/atsam/if_atsam.c',
    ],
    'arm/csb336': [
        'bsps/arm/csb336/net/lan91c11x.c',
        'bsps/arm/csb336/net/network.c',
    ],
    'arm/csb337': [
        'bsps/arm/csb337/net/network.c',
    ],
    'arm/edb7312': [
        'bsps/arm/edb7312/net/network.c',
    ],
    'arm/gumstix': [
        'bsps/arm/gumstix/net/rtl8019.c',
    ],
    'arm/lpc24xx_ea': [
        'bsps/arm/shared/lpc-ethernet.c',
    ],
    'arm/rtl22xx': [
        'bsps/arm/rtl22xx/net/network.c',
    ],
    'bfin/bf537Stamp': [
        'bsps/bfin/bf537Stamp/net/ethernet.c',
        'bsps/bfin/bf537Stamp/net/networkconfig.c',
    ],
    'i386/pc386': [
        'bsps/i386/pc386/net/3c509.c',
        'bsps/i386/pc386/net/elink.c',
        'bsps/i386/pc386/net/ne2000.c',
        'bsps/i386/pc386/net/wd8003.c',
    ],
    'lm32/lm32_evr': [
        'bsps/lm32/shared/net/network.c',
        'bsps/lm32/shared/net/tsmac.c',
    ],
    'm68k/av5282': [
        'bsps/m68k/av5282/net/network.c',
    ],
    'm68k/csb360': [
        'bsps/m68k/csb360/net/network.c',
    ],
    'm68k/mcf5235': [
        'bsps/m68k/mcf5235/net/network.c',
    ],
    'm68k/mcf5329': [
        'bsps/m68k/mcf5329/net/network.c',
    ],
    'm68k/mvme167': [
        'bsps/m68k/mvme167/net/network.c',
    ],
    'm68k/uC5282': [
        'bsps/m68k/uC5282/net/network.c',
    ],
    'mips/csb350': [
        'bsps/mips/csb350/net/network.c',
    ],
    'powerpc/beatnik': [
        'bsps/powerpc/beatnik/net/if_em/if_em.c',
        'bsps/powerpc/beatnik/net/if_em/if_em_hw.c',
        'bsps/powerpc/beatnik/net/if_em/if_em_rtems.c',
        'bsps/powerpc/beatnik/net/if_gfe/if_gfe.c',
        'bsps/powerpc/beatnik/net/if_gfe/if_gfe_rtems.c',
        'bsps/powerpc/beatnik/net/if_mve/mv643xx_eth.c',
        'bsps/powerpc/beatnik/net/porting/if_xxx_rtems.c',
        'bsps/powerpc/beatnik/net/support/bsp_attach.c',
        'bsps/powerpc/beatnik/net/support/early_link_status.c',
    ],
    'powerpc/mpc8260ads': [
        'bsps/powerpc/mpc8260ads/net/if_hdlcsubr.c',
        'bsps/powerpc/mpc8260ads/net/network.c',
    ],
    'powerpc/mvme3100': [
        'bsps/powerpc/mvme3100/net/tsec.c',
    ],
    'powerpc/mvme5500': [
        'bsps/powerpc/mvme5500/net/if_100MHz/GT64260eth.c',
        'bsps/powerpc/mvme5500/net/if_1GHz/if_wm.c',
        'bsps/powerpc/mvme5500/net/if_1GHz/pci_map.c',
    ],
    'powerpc/psim': [
        'bsps/powerpc/psim/net/if_sim.c',
    ],
    'powerpc/virtex': [
        'bsps/powerpc/virtex/net/xiltemac.c',
    ],
    'riscv/griscv': [
        'bsps/riscv/griscv/net/griscv_greth.c',
        'bsps/shared/grlib/net/greth.c',
        'bsps/shared/grlib/net/greth.c',
        'bsps/shared/grlib/net/network_interface_add.c',
        'bsps/shared/grlib/net/network_interface_add.c',
    ],
    'sparc/erc32': [
        'bsps/sparc/erc32/net/erc32sonic.c',
    ],
    'sparc/leon2': [
        'bsps/shared/grlib/net/greth.c',
        'bsps/shared/grlib/net/greth.c',
        'bsps/shared/grlib/net/network_interface_add.c',
        'bsps/shared/grlib/net/network_interface_add.c',
        'bsps/sparc/leon2/net/leon_open_eth.c',
        'bsps/sparc/leon2/net/leon_smc91111.c',
    ],
    'sparc/leon3': [
        'bsps/shared/grlib/net/greth.c',
        'bsps/shared/grlib/net/greth.c',
        'bsps/shared/grlib/net/network_interface_add.c',
        'bsps/shared/grlib/net/network_interface_add.c',
        'bsps/sparc/leon3/net/leon_greth.c',
        'bsps/sparc/leon3/net/leon_open_eth.c',
        'bsps/sparc/leon3/net/leon_smc91111.c',
    ],
}
