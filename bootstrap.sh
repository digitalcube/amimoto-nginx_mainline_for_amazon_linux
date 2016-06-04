#!/usr/bin/env bash

set -ex

sudo yum -y update
sudo yum -y install rpm-build git gcc make autoconf tmux
sudo yum -y install pcre-devel openssl-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  rubygem-rake bison

if [ -d ~/rpmbuild ]; then
  cd ~/rpmbuild && git fetch origin
else
  git clone https://github.com/OpsRockin/nginx_preview_for_amimoto.git ~/rpmbuild
fi
