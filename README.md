Wazo install CD
===============

This repo is deprecated
-----------------------

The procedure described here was valid until Wazo 18.03. This repo is only kept to rebuild any old ISO if necessary.

Requirements
------------

    apt-get install simple-cdd syslinux-common netpbm mtools dosfstools
    echo deb http://mirror.wazo.community/debian/ wazo-dev main > /etc/apt/sources.list.d/wazo-for-cd-build.list

Generate CD with following command:

    ./build-iso.sh

Docker
======

Min version: 1.7.0

There are 3 steps to build the ISO:

* create a bunch of directories with the right permissions on the host
* build the builder image
* run the builder image to create the ISO

32-bit
------

    ./init-docker.sh
    docker build -t xivo-cd32 -f dockerfile/32/Dockerfile .
    docker run -v /tmp/cd32/images:/home/builder/xivo-install-cd/images \
               -v /tmp/cd32:/home/builder/xivo-install-cd/tmp \
               -v /tmp/xivo_packages/:/tmp/xivo_packages/ \
               xivo-cd32

64-bit
------

    ./init-docker.sh
    docker build -t xivo-cd64 -f dockerfile/64/Dockerfile .
    docker run -v /tmp/cd64/images:/home/builder/xivo-install-cd/images \
               -v /tmp/cd64:/home/builder/xivo-install-cd/tmp \
               -v /tmp/xivo_packages/:/tmp/xivo_packages/ \
               xivo-cd64

The resulting ISO is in:

    /home/builder/xivo-install-cd/images (container)
    /tmp/cd32/images (host for 32-bit)
    /tmp/cd64/images (host for 64-bit)

Docker compose
==============

Min version: 1.3.1

    ./init-docker.sh
    docker-compose up -d

The resulting ISO is in:

    /tmp/cd32/images (host for 32-bit)
    /tmp/cd64/images (host for 64-bit)
