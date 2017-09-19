#!/bin/bash
set -x

sudo apt-get update

build_dir=$(pwd)
image_dir="$build_dir/images"
packages_dir="/tmp/xivo_packages"
mirror="http://http.us.debian.org/debian/"

cleanup () {
    rm -rf $build_dir/tmp/{cd-build,debian-cd,debootstrap,extra}
    rm -rf $build_dir/images/*
}

build_iso () {
    cd $build_dir
    ./get-xivo-packages.py $packages_dir -V rc
    simple-cdd --dist jessie --profiles-udeb-dist jessie --conf ./xivo.conf --debian-mirror $mirror --debug
    if [ $? -ne 0 ] ; then
        exit 1
    fi
}

rename_iso () {
    local version="$(basename /tmp/xivo_packages/xivo-base* | awk -F'[_~]' '{ print $2 }')"
    local arch=$(dpkg-architecture -qDEB_HOST_ARCH)
    cd $image_dir
    mv debian-*.iso wazo-$version-$arch.iso
    md5sum wazo-$version-$arch.iso > wazo-$version-$arch.iso.md5sum
}

cleanup
build_iso
rename_iso
