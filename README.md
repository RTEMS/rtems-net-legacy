RTEMS Legacy Networking stack
=============================

`rtems-net-legacy repository` contains the legacy networking stack that was a part
of the RTEMS versions through 5 and resided under cpukit/libnetworking.

This is a standalone repository containing the rtems legacy networking stack and
will be only maintained for bug fixes.  You can find additional documentation at 
https://docs.rtems.org/


rtems_waf submodule
-------------------
This repository uses rtems_waf as a git submodule. To update the submodule we
need to run the following git commands:


  ```shell
  git submodule init
  git submodule update
  ```


Building
--------

To build and install:

  ```shell
  $ ./waf configure --prefix=$HOME/development/rtems/6
  $ ./waf build install
  ```

To get help and see waf options:

  ```shell
  ./waf --help
  ```

Waf
---

The Waf project can be found here:

  https://waf.io/



LICENSE
-------
The code is licensed under a mix of the rtems.org/LICENSE and various BSD
licenses


About Legacy libnetworking
--------------------------
This is a snapshot of my attempt to fit the FreeBSD networking code into
RTEMS.  Things seem to be working!

Things that need to be done:
  1. More documentation!
  2. Figure out what's still not working :-)
  3. Rationalize the include files.  Right now I have a special
     hack in the Makefile to ensure that I pick up the FreeBSD versions
     of the include files that are duplicated between RTEMS
     and FreeBSD.

     The network device driver source should move to the BSP source tree.
  4. Have a look at all the FIXME comments.
  5. Go through and make sure that all the source files are
	   free of undesired copyright restrictions.

Initial Changes
---------------

```
19-AUG-1998 snapshot
	- Pulled BOOTP initialization out of rtems_glue.  Applications which
	  don't used BOOTP are now about 5k smaller.
	- Loopback interface is not installed by default, rather it is
	  attached like any other interface.  Saves about 0.5 kbytes.
	- Add rtems_bsdnet_show_if_stats();
	- Moved test programs from below freebsd directory.

18-AUG-1998 snapshot
	- Removed some include files that were already part of RTEMS.
	- Cleaned up machine/types.h to prepare for inclusion in RTEMS source.
	- Added syslog library routines -- much simpler than KA9Q version.
	  Sockets can be shared among tasks (as long as the send is
	  protected by a mutex) so there's no need for a Syslog Daemon.

16-AUG-1998 snapshot
	- Table-driven configuration (networkconfig.h).
	- Cleaned up rtems_bsdnet.h.
	- BOOTP now retries properly -- Note to Joel:
		The dichotomy between RTEMS and UNIX error codes is
		a real pain!

14-AUG-1998 snapshot
	- Added dummy getprotobyname() and getprotobynum() functions.
	- Added socket ioctl.
	- Added application-level entry to manipulate routing tables.
	- Added non-BOOTP network initialization.

13-AUG-1998 snapshot
	- Changed some BOOTP addresses from sockaddr_in to inaddr;
	- Get DNS information from BOOTP reply.
	- Got DNS lookups working.
	  Bloatware comes to RTEMS -- invoking gethostbyname() drags in
	  and extra 40 kbytes of code!
	- Added hostname lookup program.

12-AUG-1998 snapshot
	- Added startup delay to network initialization.
	- More statistic-printing routines.
	- Added TFTP driver and test program
	- Modified TFTP test program to use networkconfig.h.
	- Removed unused include files.
	- Added from ftp://ftp.ca.FreeBSD.ORG/pub/FreeBSD/FreeBSD-current/src/lib/libc/net.

11-AUG-1998 snapshot.
	- Added getpeername()
	- Added M68k versions of IP checksum code
	- Added TCP timing program to snapshot.

02-AUG-1998 snapshot.
```
