Summary: Samba SMB client and server
Name: samba
Version: 2.2.12
Release: 1
Copyright: GNU GPL version 2
Group: Networking
Source: http://download.samba.org/samba/ftp/samba-%{version}.tar.bz2
Packager: Gerald Carter [Samba-Team] <jerry@samba.org>
Requires: pam >= 0.72 kernel >= 2.2.1 glibc >= 2.1.2
Prereq: chkconfig fileutils
Provides: samba = %{version}
BuildPreReq: libtool
Obsoletes: samba-common, samba-client, samba-swat
BuildRoot: /var/tmp/samba
Prefix: /usr

%description
Samba provides an SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients, including various versions of MS Windows, OS/2,
and other Linux machines. Samba also provides some SMB
clients, which complement the built-in SMB filesystem
in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba-2.2 features working NT Domain Control capability and 
includes the SWAT (Samba Web Administration Tool) that 
allows samba's smb.conf file to be remotely managed using your 
favourite web browser. For the time being this is being
enabled on TCP port 901 via inetd.

Users are advised to use Samba-2.2 as a Windows NT4
Domain Controller only on networks that do NOT have a Windows
NT Domain Controller. This release does NOT as yet have
Backup Domain control ability.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.

NOTE: Red Hat Linux uses PAM which has integrated support
for Shadow passwords and quotas. Do NOT recompile with the
SHADOW_PWD option enabled

%changelog
* Thu Jun 6 2002 Gerald Carter <jerry@samba.org>
  - add separate winbindd init script
  - build and install libsmbclient

* Sun Jun 2 2002 Gerald Carter <jerry@samba.org>
  - include audit and recycle VFS modules in /usr/lib/samba

* Mon May 6 2002 Gerald Carter <jerry@samba.org>
  - moved findsmb to a standard component in samba's 
    "make install".  Removed from specfile.
 
* Sun Oct 14 2001 Andrew Bartlett <abartlet@samba.org>
 - Set SBINDIR for codepage/manpage install, cope with 
    broken Makefile

* Mon Aug 1 2001 Tim Potter <tpot@samba.org>
 - Install winbind daemon, client programs, nss and pam libraries

* Sat Mar 31 2001 Andrew Bartlett <abartlet@pcug.org.au>
 - Changed prefix/share/man for _mandir/share/man
  - Changed this for a sed macro MANDIR_MACRO
  - This allows us to build both RH7 (RPM4)
     and older versions from same specfile.
 - Made makerpms.sh use the rpm -ta command rather 
    than attempting to devine the correct location to 
    put the file.  Also removes some /tmp symlink games.
  - Allows build on RPM4
 - Increased PAM requirements to allow us to use 
   system-auth (this pam is in 6.x errata at least)

* Tue Mar 27 2001 John H Terpstra <jht@samba.org>
 - Fixed typos introduced by Sum Wun.
 - Build for Red Hat 7.x

* Sun Nov 12 2000 John H Terpstra <jht@samba.org>
 - Updated for Samba-2.2 releases
 - Added libnss_wins.so stuff
 - Added compile-time options

* Sat Nov 29 1999 Matthew Vanecek <mev0003@unt.edu>
 - Added a Prefix and changed "/usr" to "%{prefix}"

* Sat Nov 11 1999 Tridge <tridge@linuxcare.com>
 - changed from mount.smb to mount.smbfs

* Sat Oct 9 1999 Tridge <tridge@linuxcare.com>
 - removed smbwrapper
 - added smbmnt and smbmount

* Sun Apr 25 1999 John H Terpstra <jht@samba.org>
 - added smbsh.1 man page

* Fri Mar 26 1999 Andrew Tridgell <tridge@samba.org>
 - added --with-pam as pam is no longer used by default

* Sat Jan 27 1999 Jeremy Allison <jra@samba.org>
 - Removed smbrun binary and tidied up some loose ends

* Sun Oct 25 1998 John H Terpstra <jht@samba.org>
 - Added parameters to /config to ensure smb.conf, lmhosts, 
	and smbusers never gets over-written.

* Sat Oct 24 1998 John H Terpstra <jht@samba.org>
 - removed README.smbsh file from docs area

* Mon Oct 05 1998 John H Terpstra <jht@samba.org>
 - Added rpcclient to binaries list
 - Added smbwrapper stuff

* Fri Aug 21 1998 John H Terpstra <jht@samba.org>
 - Updated for Samba version 2.0 building

* Tue Jul 07 1998 Erik Troan <ewt@redhat.com>
  - updated postun triggerscript to check $0
  - clear /etc/codepages from %preun instead of %postun

* Sat Jul 04 1998 John H Terpstra <jht@samba.org>
 - fixed codepage preservation during update via -Uvh

* Mon Jun 08 1998 Erik Troan <ewt@redhat.com>
  - made the %postun script a tad less agressive; no reason to remove
    the logs or lock file 
  - the %postun and %preun should only exectute if this is the final
    removal
  - migrated %triggerpostun from Red Hat's samba package to work around
    packaging problems in some Red Hat samba releases

* Sun Apr 26 1998 John H Terpstra <jht@samba.org>
 - Tidy up for early alpha releases
 - added findsmb from SGI packaging

* Thu Apr 09 1998 John H Terpstra <jht@samba.org>
 - Updated spec file
 - Included new codepage.936

* Sat Mar 20 1998 John H Terpstra <jht@samba.org>
 - Added swat facility

* Sat Jan 24 1998 John H Terpstra <jht@samba.org>
 - Many optimisations (some suggested by Manoj Kasichainula <manojk@io.com>
  - Use of chkconfig in place of individual symlinks to /etc/rc.d/init/smb
  - Compounded make line
  - Updated smb.init restart mechanism
  - Use compound mkdir -p line instead of individual calls to mkdir
  - Fixed smb.conf file path for log files
  - Fixed smb.conf file path for incoming smb print spool directory
  - Added a number of options to smb.conf file
  - Added smbuser file and smb.conf file updates for username map

%prep
%setup

%build
## Build main Samba source
cd source

%ifarch ia64
libtoolize --copy --force     # get it to recognize IA-64
autoheader
autoconf
EXTRA="-D_LARGEFILE64_SOURCE"
%endif
NUMCPU=`grep processor /proc/cpuinfo | wc -l`
CFLAGS="$RPM_OPT_FLAGS $EXTRA" ./configure \
	--prefix=%{prefix} \
	--localstatedir=/var \
	--with-configdir=/etc/samba \
	--with-privatedir=/etc/samba \
	--with-codepagedir=/etc/codepages \
	--with-fhs \
	--with-quotas \
	--with-msdfs \
	--with-smbmount \
	--with-pam \
	--with-pam_smbpass \
	--with-syslog \
	--with-utmp \
	--with-sambabook=%{prefix}/share/swat/using_samba \
	--with-swatdir=%{prefix}/share/swat \
	--with-libsmbclient 
make -j${NUMCPU} proto
make -j${NUMCPU} all nsswitch/libnss_wins.so
make -j${NUMCPU} debug2html
make -j${NUMCPU} bin/smbspool

## Build VFS modules
cd ../examples/VFS
CFLAGS="$RPM_OPT_FLAGS $EXTRA" ./configure \
        --prefix=%{prefix} \
        --localstatedir=/var
make
cd ../..

# Remove some permission bits to avoid to many dependencies
find examples docs -type f | xargs -r chmod -x

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/etc/samba
mkdir -p $RPM_BUILD_ROOT/etc/codepages/src
mkdir -p $RPM_BUILD_ROOT/etc/{logrotate.d,pam.d,samba}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{prefix}/{bin,sbin}
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/swat/{images,help,include,using_samba}
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/swat/using_samba/{figs,gifs}
mkdir -p $RPM_BUILD_ROOTMANDIR_MACRO
mkdir -p $RPM_BUILD_ROOT/var/cache/samba
mkdir -p $RPM_BUILD_ROOT/var/{log,run}/samba
mkdir -p $RPM_BUILD_ROOT/var/spool/samba
mkdir -p $RPM_BUILD_ROOT/lib/security
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/samba/vfs
mkdir -p $RPM_BUILD_ROOT%{prefix}/{lib,include}

# Install standard binary files
for i in nmblookup smbclient smbpasswd smbstatus testparm testprns \
      make_smbcodepage make_unicodemap make_printerdef rpcclient smbspool \
      smbcacls smbcontrol wbinfo smbmnt
do
install -m755 source/bin/$i $RPM_BUILD_ROOT%{prefix}/bin
done
for i in mksmbpasswd.sh smbtar findsmb
do
	install -m755 source/script/$i $RPM_BUILD_ROOT%{prefix}/bin
done

# Install secure binary files
for i in smbd nmbd swat smbmount smbumount debug2html winbindd
do
	install -m755 source/bin/$i $RPM_BUILD_ROOT%{prefix}/sbin
done

# we need a symlink for mount to recognise the smb and smbfs filesystem types
ln -sf %{prefix}/sbin/smbmount $RPM_BUILD_ROOT/sbin/mount.smbfs
ln -sf %{prefix}/sbin/smbmount $RPM_BUILD_ROOT/sbin/mount.smb

# This allows us to get away without duplicating code that 
#  sombody else can maintain for us.  
cd source
make BASEDIR=$RPM_BUILD_ROOT/usr \
	LIBDIR=$RPM_BUILD_ROOT/etc/samba \
	VARDIR=$RPM_BUILD_ROOT/var \
	SBINDIR=$RPM_BUILD_ROOT%{prefix}/sbin \
	BINDIR=$RPM_BUILD_ROOT%{prefix}/bin \
	MANDIR=$RPM_BUILD_ROOTMANDIR_MACRO \
	CODEPAGEDIR=$RPM_BUILD_ROOT/etc/codepages \
	SWATDIR=$RPM_BUILD_ROOT/usr/share/swat \
	SAMBABOOK=$RPM_BUILD_ROOT/usr/share/swat/using_samba \
	installman installcp installswat
cd ..

# Install codepage source files
for i in source/codepages/codepage_def.* source/codepages/*.TXT
do
	install -m644 $i $RPM_BUILD_ROOT/etc/codepages/src
done

# Install the nsswitch wins library
install -m755 source/nsswitch/libnss_wins.so $RPM_BUILD_ROOT/lib
( cd $RPM_BUILD_ROOT/lib; ln -sf libnss_wins.so libnss_wins.so.2; )

# Install winbind shared libraries
install -m755 source/nsswitch/libnss_winbind.so $RPM_BUILD_ROOT/lib
( cd $RPM_BUILD_ROOT/lib; ln -sf libnss_winbind.so libnss_winbind.so.2; )
install -m755 source/nsswitch/pam_winbind.so $RPM_BUILD_ROOT/lib/security

# Install pam_smbpass.so
install -m755 source/bin/pam_smbpass.so $RPM_BUILD_ROOT/lib/security

# Install the VFS modules
install -m755 examples/VFS/recycle/recycle.so $RPM_BUILD_ROOT%{prefix}/lib/samba/vfs
install -m644 examples/VFS/recycle/recycle.conf $RPM_BUILD_ROOT/etc/samba/
install -m755 examples/VFS/block/block.so $RPM_BUILD_ROOT%{prefix}/lib/samba/vfs
install -m644 examples/VFS/block/samba-block.conf $RPM_BUILD_ROOT/etc/samba/
install -m755 examples/VFS/audit.so $RPM_BUILD_ROOT%{prefix}/lib/samba/vfs

# clean out VFS directory since it will get installed as documentation later
(cd examples/VFS; make clean)

# libsmbclient
install -m 755 source/bin/libsmbclient.so $RPM_BUILD_ROOT%{prefix}/lib/
install -m 755 source/bin/libsmbclient.a $RPM_BUILD_ROOT%{prefix}/lib/
install -m 644 source/include/libsmbclient.h $RPM_BUILD_ROOT%{prefix}/include/

# Install SWAT helper files
for i in swat/help/*.html docs/htmldocs/*.html
do
	install -m644 $i $RPM_BUILD_ROOT%{prefix}/share/swat/help
done
for i in swat/images/*.gif
do
	install -m644 $i $RPM_BUILD_ROOT%{prefix}/share/swat/images
done
for i in swat/include/*.html
do
	install -m644 $i $RPM_BUILD_ROOT%{prefix}/share/swat/include
done

# Install the miscellany
install -m644 swat/README $RPM_BUILD_ROOT%{prefix}/share/swat
install -m755 packaging/RedHat/smbprint $RPM_BUILD_ROOT%{prefix}/bin
install -m755 packaging/RedHat/smb.init $RPM_BUILD_ROOT/etc/rc.d/init.d/smb
install -m755 packaging/RedHat/winbind.init $RPM_BUILD_ROOT/etc/rc.d/init.d/winbind
install -m755 packaging/RedHat/smb.init $RPM_BUILD_ROOT%{prefix}/sbin/samba
install -m644 packaging/RedHat/samba.log $RPM_BUILD_ROOT/etc/logrotate.d/samba
install -m644 packaging/RedHat/smb.conf $RPM_BUILD_ROOT/etc/samba/smb.conf
install -m644 packaging/RedHat/smbusers $RPM_BUILD_ROOT/etc/samba/smbusers
install -m644 packaging/RedHat/samba.pamd $RPM_BUILD_ROOT/etc/pam.d/samba
install -m644 packaging/RedHat/samba.pamd.stack $RPM_BUILD_ROOT/etc/samba/samba.stack
install -m644 packaging/RedHat/samba.xinetd $RPM_BUILD_ROOT/etc/samba/samba.xinetd
echo 127.0.0.1 localhost > $RPM_BUILD_ROOT/etc/samba/lmhosts

# Remove "*.old" files
find $RPM_BUILD_ROOT -name "*.old" -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smb
/sbin/chkconfig --add winbind
/sbin/chkconfig smb off
/sbin/chkconfig winbind off

echo "Looking for old /etc/smb.conf..."
if [ -f /etc/smb.conf -a ! -f /etc/samba/smb.conf ]; then
	echo "Moving old /etc/smb.conf to /etc/samba/smb.conf"
	mv /etc/smb.conf /etc/samba/smb.conf
fi

echo "Looking for old /etc/smbusers..."
if [ -f /etc/smbusers -a ! -f /etc/samba/smbusers ]; then
	echo "Moving old /etc/smbusers to /etc/samba/smbusers"
	mv /etc/smbusers /etc/samba/smbusers
fi

echo "Looking for old /etc/lmhosts..."
if [ -f /etc/lmhosts -a ! -f /etc/samba/lmhosts ]; then
	echo "Moving old /etc/lmhosts to /etc/samba/lmhosts"
	mv /etc/lmhosts /etc/samba/lmhosts
fi

echo "Looking for old /etc/MACHINE.SID..."
if [ -f /etc/MACHINE.SID -a ! -f /etc/samba/MACHINE.SID ]; then
	echo "Moving old /etc/MACHINE.SID to /etc/samba/MACHINE.SID"
	mv /etc/MACHINE.SID /etc/samba/MACHINE.SID
fi

echo "Looking for old /etc/smbpasswd..."
if [ -f /etc/smbpasswd -a ! -f /etc/samba/smbpasswd ]; then
	echo "Moving old /etc/smbpasswd to /etc/samba/smbpasswd"
	mv /etc/smbpasswd /etc/samba/smbpasswd
fi

#
# For 2.2.1 we move the tdb files from /var/lock/samba to /var/cache/samba
# to preserve across reboots.
#
echo "Moving tdb files in /var/lock/samba/*.tdb to /var/cache/samba/*.tdb"
for i in /var/lock/samba/*.tdb
do
if [ -f $i ]; then
	newname=`echo $i | sed -e's|var\/lock\/samba|var\/cache\/samba|'`
	echo "Moving $i to $newname"
	mv $i $newname
fi
done

# Remove the transient tdb files.
if [ -e /var/cache/samba/brlock.tdb ]; then
	rm -f /var/cache/samba/brlock.tdb
fi

if [ -e /var/cache/samba/unexpected.tdb ]; then
	rm -f /var/cache/samba/unexpected.tdb
fi

if [ -e /var/cache/samba/connections.tdb ]; then
	rm -f /var/cache/samba/connections.tdb
fi

if [ -e /var/cache/samba/locking.tdb ]; then
	rm -f /var/cache/samba/locking.tdb
fi

if [ -e /var/cache/samba/messages.tdb ]; then
	rm -f /var/cache/samba/messages.tdb
fi

if [ -d /var/lock/samba ]; then
	rm -rf /var/lock/samba
fi

# Add swat entry to /etc/services if not already there.
if !( grep ^[:space:]*swat /etc/services > /dev/null ) then
	echo 'swat		901/tcp				# Add swat service used via inetd' >> /etc/services
fi

# Add swat entry to /etc/inetd.conf if needed.
if [ -f /etc/inetd.conf ]; then
	if !( grep ^[:space:]*swat /etc/inetd.conf > /dev/null ) then
		echo 'swat	stream	tcp	nowait.400	root	%{prefix}/sbin/swat swat' >> /etc/inetd.conf
	killall -1 inetd || :
	fi
fi

# Add swat entry to xinetd.d if needed.
if [ -d $RPM_BUILD_ROOT/etc/xinetd.d -a ! -f /etc/xinetd.d/swat ]; then
	mv /etc/samba/samba.xinetd /etc/xinetd.d/swat
else
	rm -f /etc/samba/samba.xinetd
fi

# Install the correct version of the samba pam file, depending on pam version.
if [ -f /lib/security/pam_stack.so ]; then
	echo "Installing stack version of /etc/pam.d/samba..."
	mv /etc/samba/samba.stack /etc/pam.d/samba
else
	echo "Installing non-stack version of /etc/pam.d/samba..."
	rm -f /etc/samba/samba.stack
fi

# Create winbind nss client symlink

if [ -e /lib/libnss_winbind.so ]; then
	ln -sf /lib/libnss_winbind.so /lib/libnss_winbind.so.2
fi

%preun
if [ $1 = 0 ] ; then
	/sbin/chkconfig --del smb

	# We want to remove the browse.dat and wins.dat files so they can not interfer with a new version of samba!
	if [ -e /var/cache/samba/browse.dat ]; then
		rm -f /var/cache/samba/browse.dat
	fi
	if [ -e /var/cache/samba/wins.dat ]; then
		rm -f /var/cache/samba/wins.dat
	fi

	# Remove the transient tdb files.
	if [ -e /var/cache/samba/brlock.tdb ]; then
		rm -f /var/cache/samba/brlock.tdb
	fi

	if [ -e /var/cache/samba/unexpected.tdb ]; then
		rm -f /var/cache/samba/unexpected.tdb
	fi

	if [ -e /var/cache/samba/connections.tdb ]; then
		rm -f /var/cache/samba/connections.tdb
	fi

	if [ -e /var/cache/samba/locking.tdb ]; then
		rm -f /var/cache/samba/locking.tdb
	fi

	if [ -e /var/cache/samba/messages.tdb ]; then
		rm -f /var/cache/samba/messages.tdb
	fi

	# Remove winbind nss client symlink

	if [ -L /lib/libnss_winbind.so.2 ]; then
		rm -f /lib/libnss_winbind.so.2
	fi
fi

%postun
# Only delete remnants of samba if this is the final deletion.
if [ $1 = 0 ] ; then
    if [ -x /etc/pam.d/samba ]; then
      rm -f /etc/pam.d/samba
    fi
    if [ -e /var/log/samba ]; then
      rm -rf /var/log/samba
    fi
	if [ -e /var/cache/samba ]; then
		rm -rf /var/cache/samba
	fi

    # Remove swat entries from /etc/inetd.conf and /etc/services
    cd /etc
    tmpfile=/etc/tmp.$$
	if [ -f /etc/inetd.conf ]; then
      # preserve inetd.conf permissions.
      cp -p /etc/inetd.conf $tmpfile
      sed -e '/^[:space:]*swat.*$/d' /etc/inetd.conf > $tmpfile
      mv $tmpfile inetd.conf
	fi
    # preserve services permissions.
    cp -p /etc/services $tmpfile
    sed -e '/^[:space:]*swat.*$/d' /etc/services > $tmpfile
    mv $tmpfile /etc/services

	# Remove swat entry from /etc/xinetd.d
	if [ -f /etc/xinetd.d/swat ]; then
		rm -r /etc/xinetd.d/swat
	fi
fi

#%triggerpostun -- samba < samba-2.0.0
#if [ $0 != 0 ]; then
#    /sbin/chkconfig --add smb
#fi

%files
%defattr(-,root,root)
%doc README COPYING Manifest Read-Manifest-Now
%doc WHATSNEW.txt Roadmap
%doc docs
%doc swat/README
%doc examples
%{prefix}/sbin/smbd
%{prefix}/sbin/nmbd
%{prefix}/sbin/swat
%{prefix}/bin/smbmnt
%{prefix}/sbin/smbmount
%{prefix}/sbin/smbumount
%{prefix}/sbin/winbindd
%{prefix}/sbin/debug2html
%{prefix}/sbin/samba
/sbin/mount.smbfs
/sbin/mount.smb
%{prefix}/bin/mksmbpasswd.sh
%{prefix}/bin/smbclient
%{prefix}/bin/smbspool
%{prefix}/bin/rpcclient
%{prefix}/bin/testparm
%{prefix}/bin/testprns
%{prefix}/bin/findsmb
%{prefix}/bin/smbstatus
%{prefix}/bin/nmblookup
%{prefix}/bin/make_smbcodepage
%{prefix}/bin/make_unicodemap
%{prefix}/bin/make_printerdef
%{prefix}/bin/smbpasswd
%{prefix}/bin/smbtar
%{prefix}/bin/smbprint
%{prefix}/bin/smbcontrol
%{prefix}/bin/smbcacls
%{prefix}/bin/wbinfo
%{prefix}/bin/pam_smbpass.so
%{prefix}/bin/smbmount
%{prefix}/bin/smbumount
%{prefix}/bin/tdbbackup
%attr(755,root,root) /lib/libnss_wins.s*
%attr(755,root,root) %{prefix}/lib/samba/vfs/*.so
%{prefix}/include/libsmbclient.h
%{prefix}/lib/libsmbclient.a
%{prefix}/lib/libsmbclient.so
%{prefix}/share/swat/help/*
%{prefix}/share/swat/images/*
%{prefix}/share/swat/include/header.html
%{prefix}/share/swat/include/footer.html
%{prefix}/share/swat/using_samba/*
%{prefix}/share/swat/README
%config(noreplace) /etc/samba/lmhosts
%config(noreplace) /etc/samba/smb.conf
%config(noreplace) /etc/samba/recycle.conf
%config(noreplace) /etc/samba/samba-block.conf
%config(noreplace) /etc/samba/smbusers
/etc/samba/samba.stack
/etc/samba/samba.xinetd
/etc/rc.d/init.d/smb
/etc/rc.d/init.d/winbind
/etc/logrotate.d/samba
%config(noreplace) /etc/pam.d/samba
MANDIR_MACRO/man1/*
MANDIR_MACRO/man5/*
MANDIR_MACRO/man7/*
MANDIR_MACRO/man8/*
%dir /etc/codepages/*
%dir /etc/codepages/src/*
%attr(755,root,root) %dir /var/cache/samba
%dir /var/log/samba
%dir /var/run/samba
%attr(1777,root,root) %dir /var/spool/samba
%attr(-,root,root) /lib/libnss_winbind.so
%attr(-,root,root) /lib/security/pam_winbind.so
%attr(-,root,root) /lib/security/pam_smbpass.so
