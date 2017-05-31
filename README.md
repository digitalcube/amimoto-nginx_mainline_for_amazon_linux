

## Setup

```
$ sudo yum -y update
$ sudo yum -y install rpm-build git gcc make autoconf
$ git clone https://github.com/OpsRockin/nginx_preview_for_amimoto.git ~/rpmbuild
```

## Build

on EC2

```
$ cd ~/rpmbuild
$ sudo yum -y install pcre-devel openssl-devel libxml2-devel libxslt-devel gd-devel perl-devel perl-ExtUtils-Embed geoip-devel gperftools-devel
$ wget http://nginx.org/download/nginx-1.13.1.tar.gz -O SOURCES/nginx-1.13.1.tar.gz
$ wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
$ rpmbuild -ba SPECS/nginx.spec
```

or Docker

```
wget http://nginx.org/download/nginx-1.13.1.tar.gz -O SOURCES/nginx-1.13.1.tar.gz
wget https://github.com/OpsRockin/ngx_cache_purge/archive/2.3.dynamic.tar.gz -O SOURCES/ngx_cache_purge_2.3.dynamic.tar.gz
docker build -t local/nginx_preview_for_amimoto .
docker run --rm -v `pwd`:/root/rpmbuild:cached local/nginx_preview_for_amimoto
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


