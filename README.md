# Nginx mainline for Amazon Linux 1 and 2 with ngx_mruby

[![CircleCI](https://circleci.com/gh/OpsRockin/nginx_mainline_for_amazon_linux.svg?style=svg)](https://circleci.com/gh/OpsRockin/nginx_mainline_for_amazon_linux)

includes

- TLS1.3 support (amzn2)
- ngx_mruby
- ngx_cache_purge
- ngx_pagespeed

## Setup

```
$ sudo yum -y update
$ sudo yum -y install rpm-build git gcc make autoconf
$ git clone https://github.com/OpsRockin/nginx_preview_for_amimoto.git ~/rpmbuild
```

### Update Steps

- edit `nginx_version`
  - mod NGINX_VERSION
  - mod OPENSSL_VERSION (optional)
- edit `SPECS/nginx.spec`
  - mod Version, Release
  - mod openssl_version (optional)
  - mod ngx_mruby_rev (optional)
  - append note to `%changelog` section

## Build

on EC2 (DEPRECATED)

```
$ source ./nginx_version
$ source ./NPS_VERSION
$ source ./OPENSSL_VERSION
$ cd ~/rpmbuild
$ sudo yum -y install pcre-devel openssl-devel libxml2-devel libxslt-devel gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel
$ wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
$ wget https://codeload.github.com/apache/incubator-pagespeed-ngx/tar.gz/v${NPS_VERSION}-stable -O SOURCES/incubator-pagespeed-ngx_${NPS_VERSION}.tar.gz
$ wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
$ rpmbuild -ba SPECS/nginx.spec
```

or Docker (Current maintenance target)

```
source ./nginx_version
source ./NPS_VERSION
source ./OPENSSL_VERSION
wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}-latest.tar.gz -O SOURCES/openssl-${OPENSSL_VERSION}-latest.tar.gz
wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
wget https://codeload.github.com/apache/incubator-pagespeed-ngx/tar.gz/v${NPS_VERSION}-stable -O SOURCES/incubator-pagespeed-ngx_${NPS_VERSION}.tar.gz
wget https://dl.google.com/dl/page-speed/psol/${PSOL_VERSION}-x64.tar.gz -O SOURCES/psol_${PSOL_VERSION}.tar.gz
docker pull amazonlinux:2018.03-with-sources # to update base
docker pull amazonlinux:2-with-sources # to update base
docker build -t local/nginx_preview_for_amimoto:1 --build-arg BASE_TAG=2018.03-with-sources .
docker build -t local/nginx_preview_for_amimoto:2 .

docker run -it --rm -v `pwd`:/root/rpmbuild:cached local/nginx_preview_for_amimoto:1
docker run -it --rm -v `pwd`:/root/rpmbuild:cached local/nginx_preview_for_amimoto:2
```


## Dynamic Modules

### [ngx_mruby](https://github.com/matsumoto-r/ngx_mruby)

Add nginx.conf to enable module below.

```
load_module modules/ngx_http_mruby_module.so;
```

example

```
location /hello {
    mruby_content_handler_code '
        Nginx.rputs "hello"
        Nginx.echo "world!"
    ';
}
```


### [ngx_cache_purge](https://github.com/FRiCKLE/ngx_cache_purge)

> Notice: we include [forked version](https://github.com/OpsRockin/ngx_cache_purge) to build as dynamic module.

Add nginx.conf to enable module below.

```
load_module modules/ngx_http_cache_purge_module.so;
```


### [ngx_pagespeed](https://www.modpagespeed.com/)

check latest stable

```
curl -sS https://www.modpagespeed.com/doc/release_notes | grep release_ | head -1 | sed -e "s/^.*release_\([0-9\.]*\)-beta.*/\1/"
#=> <h2 id="release_1.12.34.3-stable">Release 1.12.34.3-stable</h2>
```

```
load_module modules/ngx_pagespeed.so;
```

```
http or server {
  pagespeed on;
  pagespeed FileCachePath /var/ngx_pagespeed_cache;

...

}
```

See https://www.modpagespeed.com/doc/configuration
