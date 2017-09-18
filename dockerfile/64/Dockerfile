FROM debian:stretch

MAINTAINER Wazo Maintainers <dev.wazo@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yqq update
RUN apt-get -yqq install simple-cdd \
                    syslinux-common \
                    netpbm \
                    sudo \
                    mtools \
                    dosfstools \
                    gnupg \
                    python \
                    debian-archive-keyring

RUN apt-key adv --recv-keys --keyserver pgp.mit.edu 0x3F1BF7FC527FBC6A

RUN groupadd builder
RUN useradd -r -g builder -G sudo -s /bin/bash -u 1000 builder
RUN mkdir -p /home/builder/
RUN echo 'builder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/builder
RUN chmod 440 /etc/sudoers.d/builder
ADD . /home/builder/xivo-install-cd
RUN chown -R builder.builder /home/builder/

WORKDIR /home/builder/xivo-install-cd
USER builder

CMD ./build-iso.sh
