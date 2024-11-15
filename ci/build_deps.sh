#!/usr/bin/env bash
set -e

# load NGINX_VERSION
source ./nginx_version
source ./NPS_VERSION

yum -y update && yum -y install rpm-build git gcc make autoconf tmux \
  pcre-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  bison wget gcc-c++ libuuid-devel

(cd /usr/local/src \
&& wget https://ftp.gnu.org/gnu/make/make-4.0.tar.gz \
&& tar xvzf make-4.0.tar.gz \
&& cd make-4.0 \
&& ./configure \
&& make \
&& make install \
&& yum erase make -y \
&& ln -s /usr/local/bin/make /usr/bin/make)


if [ "$CIRCLE_JOB" == "build1" ] ; then
  source ./OPENSSL_VERSION
  yum install -y rubygem-rake
  wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}${OPENSSL_SUBVERSION}.tar.gz -O SOURCES/openssl-${OPENSSL_VERSION}-latest.tar.gz
  wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
  wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
fi

if [ "$CIRCLE_JOB" == "build2" ] ; then
  source ./OPENSSL_VERSION
  amazon-linux-extras install -y ruby3.0
  wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}${OPENSSL_SUBVERSION}.tar.gz -O SOURCES/openssl-${OPENSSL_VERSION}-latest.tar.gz
  wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -O SOURCES/nginx-${NGINX_VERSION}.tar.gz
  wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
fi

if [ "$CIRCLE_JOB" == "test2" ] ; then
  yum -y install openssl initscripts
fi
