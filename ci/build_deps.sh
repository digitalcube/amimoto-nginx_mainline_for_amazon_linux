#!/usr/bin/env bash

NGINX_VERSION=1.13.4

yum -y update && yum -y install rpm-build git gcc make autoconf tmux \
  pcre-devel openssl-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  rubygem-rake bison wget

if [ "$CIRCLE_JOB" == "build" ] ; then
  wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
  wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
fi
