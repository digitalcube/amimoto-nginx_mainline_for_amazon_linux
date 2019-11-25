#!/bin/bash

set -xe

rpmbuild -ba SPECS/nginx.spec --define "%debug_package %{nil}"
