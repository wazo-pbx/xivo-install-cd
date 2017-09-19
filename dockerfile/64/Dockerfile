FROM debian:stretch

MAINTAINER Wazo Maintainers <dev@wazo.community>

ENV DEBIAN_FRONTEND noninteractive

RUN true \
 && apt-get -yqq update \
 && apt-get -yqq install simple-cdd \
                         syslinux-common \
                         netpbm \
                         sudo \
                         mtools \
                         dosfstools \
                         python \
                         debian-archive-keyring \
 && groupadd builder \
 && useradd -r -g builder -G sudo -s /bin/bash -u 1000 builder \
 && mkdir -p /home/builder/ \
 && echo 'builder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/builder \
 && chmod 440 /etc/sudoers.d/builder \
 && true

ADD . /home/builder/xivo-install-cd
RUN chown -R builder.builder /home/builder/

WORKDIR /home/builder/xivo-install-cd
USER builder

CMD ./build-iso.sh
