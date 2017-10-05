#!/usr/bin/env bash

# load NGINX_VERSION
source ./nginx_version
source ./NPS_VERSION

yum -y update && yum -y install rpm-build git gcc make autoconf tmux \
  pcre-devel openssl-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  rubygem-rake bison wget gcc-c++

if [ "$CIRCLE_JOB" == "build" ] ; then
  wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
  wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
  wget https://codeload.github.com/pagespeed/ngx_pagespeed/tar.gz/v${NPS_VERSION}-stable -O SOURCES/ngx_pagespeed_${NPS_VERSION}.tar.gz
  wget https://dl.google.com/dl/page-speed/psol/1.12.34.2-x64.tar.gz -O SOURCES/psol_${NPS_VERSION}.tar.gz # 1.12.34.3 do not have same version of psol
fi
