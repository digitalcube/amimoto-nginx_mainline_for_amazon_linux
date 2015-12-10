#
%dump
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1

# end of distribution specific definitions

Summary: A high performance web server and reverse proxy server(for Amimoto Wordpress preview 1.9.x)
Name: nginx
Epoch: 1
Version: 1.9.9
Release: 1%{?dist}.amimoto
Packager: OpsRock LLC
Vendor: nginx inc. via OpsRock LLC
URL: http://nginx.org/

Source0: http://nginx.org/download/%{name}-%{version}.tar.gz
Source1: logrotate
Source2: nginx.init
Source3: nginx.sysconf
Source4: nginx.conf
Source5: virtual.conf

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

%if 0%{?suse_version} == 1315
%debug_package
%endif

%prep
%setup -q

%build
./configure --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/var/run/nginx.pid --lock-path=/var/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module --with-http_image_filter_module --with-http_geoip_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_stub_status_module --with-http_perl_module --with-mail --with-mail_ssl_module --with-pcre --with-pcre-jit --with-google_perftools_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic' --with-ld-opt=' -Wl,-E' --with-http_v2_module
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

# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx

%{__rm} -rf $RPM_BUILD_ROOT/usr/local
%{__rm} $RPM_BUILD_ROOT/usr/lib64/perl5/perllocal.pod

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
%{_initrddir}/nginx

/usr/lib64/perl5/vendor_perl/auto/nginx/nginx.so
/usr/lib64/perl5/vendor_perl/nginx.pm

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx
%attr(0700,nginx,nginx) %dir %{_localstatedir}/lib/nginx
%attr(0700,nginx,nginx) %dir %{_localstatedir}/lib/nginx/tmp
%attr(0700,nginx,nginx) %dir %{_localstatedir}/log/nginx

%pre
getent group nginx > /dev/null || groupadd -r nginx
getent passwd nginx > /dev/null || \
    useradd -r -d /var/lib/nginx -g nginx \
    -s /sbin/nologin -c "Nginx web server" nginx
exit 0

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add nginx
fi
if [ $1 -eq 2 ]; then
    # Make sure these directories are not world readable.
    chmod 700 /var/lib/nginx
    chmod 700 /var/lib/nginx/tmp
    chmod 700 /var/log/nginx
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
    /sbin/service nginx stop >/dev/null 2>&1
    /sbin/chkconfig --del nginx
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service nginx upgrade || :
fi

%changelog
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
