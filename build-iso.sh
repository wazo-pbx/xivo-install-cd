#!/bin/bash
set -x

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
    simple-cdd --dist stretch --profiles-udeb-dist stretch --conf ./xivo.conf --debian-mirror $mirror --debug
    if [ $? -ne 0 ] ; then
        exit 1
    fi
}

rename_iso () {
    local arch=$(dpkg-architecture -qDEB_HOST_ARCH)
    local version="$(basename $packages_dir/xivo-base_* | awk -F'[_~]' '{ print $2 }')"
    cd $image_dir
    mv debian-*.iso wazo-$version-$arch.iso
    md5sum wazo-$version-$arch.iso > wazo-$version-$arch.iso.md5sum
}

cleanup
build_iso
rename_iso
