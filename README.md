

## Setup

```
$ sudo yum -y update
$ sudo yum -y install rpm-build git gcc make autoconf
$ git clone https://github.com/OpsRockin/nginx_preview_for_amimoto.git ~/rpmbuild
```

## Build

```
$ cd ~/rpmbuild
$ sudo yum -y install pcre-devel openssl-devel libxml2-devel libxslt-devel gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel
$ wget http://nginx.org/download/nginx-1.9.11.tar.gz -O SOURCES/nginx-1.9.11.tar.gz
$ rpmbuild -ba SPECS/nginx.spec
```
