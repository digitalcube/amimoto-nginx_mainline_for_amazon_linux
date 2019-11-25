# %amzn = 1 or 2 to check hostos version
%dump
%define nginx_home %{_localstatedir}/cache/nginx
%define systemd_dir /usr/lib/systemd/system/
%define nginx_user nginx
%define nginx_group nginx
%define mruby_dir /opt/mruby

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1

## dynamic-modules
%define ngx_cache_purge_rev 2.3.dynamic
%define ngx_pagespeed_rev 1.13.35.2
%define psol_rev 1.13.35.2
%define ngx_mruby_rev v2.1.8
%define ngx_mruby_src https://github.com/matsumoto-r/ngx_mruby.git
# end of distribution specific definitions

Summary: A high performance web server and reverse proxy server(for Amimoto Wordpress)
Name: nginx
Epoch: 1
Version: 1.17.6
Release: 2%{?dist}.amimoto
Packager: OpsRock LLC
Vendor: nginx inc. via OpsRock LLC
URL: http://nginx.org/

Source0: http://nginx.org/download/%{name}-%{version}.tar.gz
Source1: logrotate
Source2: nginx.init%{?amzn}
Source3: nginx.sysconf
Source4: nginx.conf
Source5: virtual.conf
Source6: ngx_cache_purge_%{ngx_cache_purge_rev}.tar.gz
Source7: ngx_mruby_build_config.rb
Source8: incubator-pagespeed-ngx_%{ngx_pagespeed_rev}.tar.gz
Source9: psol_%{psol_rev}.tar.gz
%if %{amzn} == 2
Source10: nginx-upgrade
%endif

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: gd-devel
BuildRequires: perl-devel
BuildRequires: perl-ExtUtils-Embed
BuildRequires: geoip-devel
BuildRequires: gperftools-devel

Provides: webserver

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server. Includes default keypairs for TLS.

%package        mod-http_cache_purge23
Summary:        Dinamic built http_cache_purge module for %{name}.
Requires:       %{name} >= 1.9.11

%description    mod-http_cache_purge23
Dinamic built http_cache_purge module for %{name}.

%package        mod-ngx_pagespeed
Summary:        Dinamic built ngx_pagespeed module for %{name}.
Requires:       %{name} >= 1.9.11

%description    mod-ngx_pagespeed
Dinamic built ngx_pagespeed module for %{name}.

%package        mod-ngx_mruby
Summary:        Dinamic built ngx_mruby %{ngx_mruby_rev} module for %{name}.
Requires:       %{name} >= 1.9.11

%description    mod-ngx_mruby
Dinamic built ngx_mruby %{ngx_mruby_rev} module for %{name}.
Avalable modules are...
// ngx_mruby extended classes
  - ngx_mruby_mrblib
  - rack-based-api
// mrbgems
  - iij/mruby-io
  - iij/mruby-env
  - iij/mruby-dir
  - iij/mruby-digest
  - iij/mruby-process
  - iij/mruby-pack
  - iij/mruby-socket
  - mattn/mruby-json
  - mattn/mruby-onig-regexp
  - matsumoto-r/mruby-redis
  - matsumoto-r/mruby-vedis
  - matsumoto-r/mruby-sleep
  - matsumoto-r/mruby-userdata
  - matsumoto-r/mruby-uname
  - matsumoto-r/mruby-mutex
  - matsumoto-r/mruby-localmemcache
  - matsumoto-r/mruby-httprequest

# %debug_package %{nil}

%prep
%setup -q -a 6 -a 8
# extract psol
cd incubator-pagespeed-ngx-%{ngx_pagespeed_rev}-stable
%{__tar} -xzf %{SOURCE9}
## should use Release force
sed -e "s@buildtype=Debug@buildtype=Release@g" config -i
cd -

# Start Building mruby
git clone %{ngx_mruby_src} -b %{ngx_mruby_rev} --depth 1
cd ngx_mruby
%{__cp} -f %{SOURCE7} ./
./configure --with-ngx-src-root=../ --enable-dynamic-module
make build_mruby -j 4
make generate_gems_config_dynamic
# End Building mruby

%build
export PSOL_BINARY=${RPM_BUILD_DIR}/%{name}-%{version}/incubator-pagespeed-ngx-%{ngx_pagespeed_rev}-stable/psol/lib/Release/linux/x64/pagespeed_automatic.a
./configure \
  --prefix=/usr/share/nginx \
  --sbin-path=/usr/sbin/nginx \
  --conf-path=/etc/nginx/nginx.conf \
  --error-log-path=/var/log/nginx/error.log \
  --http-log-path=/var/log/nginx/access.log \
  --http-client-body-temp-path=/var/lib/nginx/tmp/client_body \
  --http-proxy-temp-path=/var/lib/nginx/tmp/proxy \
  --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi \
  --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi \
  --http-scgi-temp-path=/var/lib/nginx/tmp/scgi \
  --pid-path=/var/run/nginx.pid \
  --lock-path=/var/lock/subsys/nginx \
  --user=nginx --group=nginx \
  --with-file-aio \
  --with-http_ssl_module \
  --with-http_realip_module \
  --with-http_addition_module \
  --with-http_xslt_module \
  --with-http_image_filter_module \
  --with-http_geoip_module \
  --with-http_sub_module \
  --with-http_dav_module \
  --with-http_flv_module \
  --with-http_mp4_module \
  --with-http_gunzip_module \
  --with-http_gzip_static_module \
  --with-http_random_index_module \
  --with-http_secure_link_module \
  --with-http_degradation_module \
  --with-http_stub_status_module \
  --with-http_perl_module \
  --with-mail \
  --with-mail_ssl_module \
  --with-pcre \
  --with-pcre-jit \
  --with-google_perftools_module \
  --with-debug \
  --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic' \
  --with-ld-opt='-Wl,-E' \
  --with-http_v2_module \
  --with-stream \
  --with-stream_ssl_module \
  --without-stream_access_module \
  --add-dynamic-module=$RPM_BUILD_DIR/%{name}-%{version}/ngx_cache_purge-%{ngx_cache_purge_rev} \
  --add-dynamic-module=$RPM_BUILD_DIR/%{name}-%{version}/incubator-pagespeed-ngx-%{ngx_pagespeed_rev}-stable \
  --add-module=$RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby/dependence/ngx_devel_kit \
  --add-dynamic-module=$RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby \
  --with-threads
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d

%{__cp} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf.default
%{__cp} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi_params $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi_params.default
%{__cp} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/mime.types $RPM_BUILD_ROOT%{_sysconfdir}/nginx/mime.types.default
%{__cp} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/scgi_params $RPM_BUILD_ROOT%{_sysconfdir}/nginx/scgi_params.default
%{__cp} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/uwsgi_params $RPM_BUILD_ROOT%{_sysconfdir}/nginx/uwsgi_params.default

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/lib/nginx/tmp

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/virtual.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

# install Perl Modules
%{__mkdir} -p $RPM_BUILD_ROOT/usr/lib64/perl5/vendor_perl/auto/nginx
%{__install} -p $RPM_BUILD_ROOT/usr/local/lib64/perl5/auto/nginx/nginx.so \
   $RPM_BUILD_ROOT/usr/lib64/perl5/vendor_perl/auto/nginx/nginx.so
%{__install} -p $RPM_BUILD_ROOT/usr/local/lib64/perl5/nginx.pm \
   $RPM_BUILD_ROOT/usr/lib64/perl5/vendor_perl/nginx.pm

%if %{amzn} == 1
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif

%if %{amzn} == 2
# install systemd service
%{__mkdir} -p $RPM_BUILD_ROOT%{systemd_dir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{systemd_dir}/nginx.service
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin/
%{__install} -m755 %{SOURCE10} \
   $RPM_BUILD_ROOT/usr/bin/nginx-upgrade
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx

%{__rm} -rf $RPM_BUILD_ROOT/usr/local
%{__rm} $RPM_BUILD_ROOT/usr/lib64/perl5/perllocal.pod

# install mruby binaries
%{__mkdir} -p $RPM_BUILD_ROOT%{mruby_dir}/bin
%{__install} -p $RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby/mruby/bin/mruby-config \
   $RPM_BUILD_ROOT%{mruby_dir}/bin/mruby-config
%{__install} -p $RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby/mruby/bin/mirb \
   $RPM_BUILD_ROOT%{mruby_dir}/bin/mirb
%{__install} -p $RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby/mruby/bin/mruby \
   $RPM_BUILD_ROOT%{mruby_dir}/bin/mruby
%{__install} -p $RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby/mruby/bin/mrbc \
   $RPM_BUILD_ROOT%{mruby_dir}/bin/mrbc
%{__install} -p $RPM_BUILD_DIR/%{name}-%{version}/ngx_mruby/mruby/bin/mruby-strip \
   $RPM_BUILD_ROOT%{mruby_dir}/bin/mruby-strip

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/default.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf.default
%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf
%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/nginx/conf.d/virtual.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/mime.types.default
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx

%if %{amzn} == 1
%{_initrddir}/nginx
%endif

%if %{amzn} == 2
%{systemd_dir}/nginx.service
/usr/bin/nginx-upgrade
%endif

/usr/lib64/perl5/vendor_perl/auto/nginx/nginx.so
/usr/lib64/perl5/vendor_perl/nginx.pm

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*
%dir %{_datadir}/nginx/modules

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0700,nginx,nginx) %dir %{_localstatedir}/lib/nginx
%attr(0700,nginx,nginx) %dir %{_localstatedir}/lib/nginx/tmp
%attr(0700,nginx,nginx) %dir %{_localstatedir}/log/nginx

%files mod-http_cache_purge23
%{_datadir}/nginx/modules/ngx_http_cache_purge_module.so

%files mod-ngx_mruby
%{_datadir}/nginx/modules/ngx_http_mruby_module.so
%{mruby_dir}/bin/mruby-config
%{mruby_dir}/bin/mirb
%{mruby_dir}/bin/mruby
%{mruby_dir}/bin/mrbc
%{mruby_dir}/bin/mruby-strip

%files mod-ngx_pagespeed
%{_datadir}/nginx/modules/ngx_pagespeed.so

%pre
getent group nginx > /dev/null || groupadd -r nginx
getent passwd nginx > /dev/null || \
    useradd -r -d /var/lib/nginx -g nginx \
    -s /sbin/nologin -c "Nginx web server" nginx
exit 0

%post
if [ $1 -eq 1 ]; then
%if %{amzn} == 1
    /sbin/chkconfig --add nginx
%endif
%if %{amzn} == 2
   systemctl preset nginx.service >/dev/null 2>&1 || :
%endif
fi

if [ $1 -eq 2 ]; then
    # Make sure these directories are not world readable.
    chmod 700 /var/lib/nginx
    chmod 700 /var/lib/nginx/tmp
    chmod 700 /var/log/nginx
%if %{amzn} == 2
   find /etc/rc.d/ -name '*nginx' -delete
   systemctl preset nginx.service >/dev/null 2>&1 || :
%endif
fi

# Create default KeyPair
umask 077
if [ -f /etc/pki/tls/private/amimoto.default.key -o -f /etc/pki/tls/certs/amimoto.default.crt ]; then
   exit 0
fi

if [ ! -f /etc/pki/tls/private/amimoto.default.key ] ; then
/usr/bin/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 2048 > /etc/pki/tls/private/amimoto.default.key 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=amimoto.default.localdomain
fi

if [ ! -f /etc/pki/tls/certs/amimoto.default.crt ] ; then
cat << EOF | /usr/bin/openssl req -new -key /etc/pki/tls/private/amimoto.default.key \
         -x509 -days 3650 -set_serial $RANDOM \
         -out /etc/pki/tls/certs/amimoto.default.crt 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
amimoto@${FQDN}
EOF
fi

%preun
if [ $1 -eq 0 ]; then
%if %{amzn} == 1
    /sbin/service nginx stop >/dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
%if %{amzn} == 2
   systemctl --no-reload disable nginx.service > /dev/null 2>&1 || :
   systemctl stop nginx.service > /dev/null 2>&1 || :
%endif
fi

%postun
if [ $1 -ge 1 ]; then
%if %{amzn} == 1
    /sbin/service nginx upgrade || :
%endif
%if %{amzn} == 2
   /usr/bin/nginx-upgrade >/dev/null 2>&1 || :
%endif
fi

%changelog
* Fri Nov 22 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.6.2: change SYSV to Systemd
* Wed Nov 20 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.6
- ngx_mruby 2.1.8
* Thu Oct 24 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.5
- ngx_mruby 2.1.7
* Tue Oct 01 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.4
- ngx_mruby 2.1.6
* Thu Aug 15 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.3
* Wed Jul 24 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.2
- ngx_mruby 2.1.5
* Wed Jun 26 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.1
* Wed May 22 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.17.0
* Thu Apr 18 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.12
* Wed Apr 03 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.10
- ngx_mruby 2.1.4
* Thu Feb 28 2019 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.9
* Wed Dec 26 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.8
* Wed Nov 28 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.7
- ngx_mruby 2.1.3
* Wed Nov 07 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.6
* Wed Oct 03 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.5
* Wed Sep 26 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.4
- ngx_mruby 2.1.2
* Thu Aug 30 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.3
* Mon Aug 13 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- ngx_mruby 2.1.1
* Wed Jul 25 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.2
* Thu Jul 05 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.1
* Tue Jul 03 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.15.0
- ngx_mruby 2.0.4
- update description
* Wed Apr 04 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.11
* Wed Mar 21 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.10
- ngx_mruby 1.20.2
* Wed Feb 21 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- ngx_pagespped 1.13.35.2
* Wed Feb 21 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.9
* Thu Jan 25 2018 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.8
* Thu Nov 30 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.7
* Thu Oct 12 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.6
* Thu Oct 05 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- ngx_mruby 1.20.1
- add dynamic module Google PageSpeed 1.12.34.3
* Fri Sep 08 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.5
* Wed Aug 09 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.4
- ngx_mruby 1.20.0
* Wed Jul 12 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- ngx_mruby 1.19.5
* Wed Jul 12 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.3
* Wed Jun 28 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.2
* Wed May 31 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.1
* Wed Apr 26 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.13.0
- ngx_mruby 1.19.4
* Mon Apr 10 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.13
* Sun Mar 26 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.12
* Fri Mar 24 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.11
- ngx_mruby 1.19.2
* Thu Feb 16 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.10
- ngx_mruby 1.18.10
* Wed Jan 25 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.9
* Wed Jan 04 2017 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.8
* Sat Dec 17 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.7
- add –with-threads  to build option
* Tue Nov 22 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.6
* Wed Oct 12 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.5
- Include Dynamic Module ngx_mruby v1.18.7
* Mon Jun 6 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.1-2
- Include Dynamic Module ngx_mruby v1.17.2
* Wed Jun 1 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.1
* Wed May 25 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.11.0
* Wed Apr 20 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.15
* Wed Apr 06 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.14
* Wed Mar 30 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.13
* Mon Feb 29 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.12 rev 3
- build ngx_cache_purge 2.3 as dynamic
* Fri Feb 26 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.12 rev 2
- enable stream modules
* Thu Feb 25 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.12
* Wed Feb 10 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.11
* Wed Jan 27 2016 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.10
* Thu Dec 10 2015 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.9
* Wed Dec 9 2015 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.8
* Mon Nov 30 2015 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.7
* Wed Nov 11 2015 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.6
* Fri Oct 23 2015 Yukihiko Sawanobori <sawanoboriyu@higanworks.com>
- 1.9.5
