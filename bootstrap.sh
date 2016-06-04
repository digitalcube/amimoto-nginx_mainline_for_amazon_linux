#!/usr/bin/env bash

set -ex

sudo yum -y update
sudo yum -y install rpm-build git gcc make autoconf tmux
sudo yum -y install pcre-devel openssl-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  rubygem-rake bison

if [ ! -d /home/ec2-user/rpmbuild ]; then
  git clone https://github.com/OpsRockin/nginx_preview_for_amimoto.git /home/ec2-user/rpmbuild
  chown -R ec2-user.ec2-user /home/ec2-user/rpmbuild
fi
