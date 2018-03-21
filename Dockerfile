FROM amazonlinux:2017.09-with-sources

RUN yum -y update && yum -y install rpm-build git gcc make autoconf tmux \
  pcre-devel openssl-devel libxml2-devel libxslt-devel \
  gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel \
  rubygem-rake bison gcc-c++ libuuid-devel

RUN mkdir -p /root/rpmbuild

WORKDIR /root/rpmbuild
# should mount currentDir with '-v `pwd`:/root/rpmbuild'
CMD ["./build.sh"]
