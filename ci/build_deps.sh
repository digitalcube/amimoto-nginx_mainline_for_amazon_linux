#!/usr/bin/env bash
set -e

# load NGINX_VERSION
source ./nginx_version
source ./NPS_VERSION

yum -y update && yum -y install rpm-build git gcc make autoconf tmux \
  pcre-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  rubygem-rake bison wget gcc-c++ libuuid-devel

if [ "$CIRCLE_JOB" == "build1" ] ; then
  source ./OPENSSL_VERSION
  wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}${OPENSSL_SUBVERSION}.tar.gz -O SOURCES/openssl-${OPENSSL_VERSION}-latest.tar.gz
  wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
  wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
fi

if [ "$CIRCLE_JOB" == "build2" ] ; then
  source ./OPENSSL_VERSION
  wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}${OPENSSL_SUBVERSION}.tar.gz -O SOURCES/openssl-${OPENSSL_VERSION}-latest.tar.gz
  wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
  wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
fi

if [ "$CIRCLE_JOB" == "test2" ] ; then
  yum -y install openssl initscripts
fi
