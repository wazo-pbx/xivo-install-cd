#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010-2018 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import with_statement

import hashlib
import os
import platform
import subprocess
import sys
import urllib2

from optparse import OptionParser

HTTP_MIRROR = 'http://mirror.wazo.community'


def main():
    GetWazoPackages().list_and_download_packages()


class GetWazoPackages(object):

    def __init__(self):
        self._parse_arguments()
        self._define_version()
        self._whitelist()
        self.stats = {'size': 0, 'installed-size': 0}
        self.packages = {}
        self.mirror = '%s/%s' % (HTTP_MIRROR, self.release)

    def list_and_download_packages(self):
        self._list_packages()
        if self.options.list:
            self._print_list()
        self._download_packages()

    def _get_architecture(self):
        arch = platform.architecture()[0]
        if arch == '64bit':
            architecture = 'amd64'
        elif arch == '32bit':
            architecture = 'i386'
        else:
            raise ('Unknown architecture!')
        return architecture

    def _parse_arguments(self):
        usage = "Usage: %prog [options] path/to/download"
        self.parser = OptionParser(usage=usage)
        self.parser.add_option('-l',
                               '--list-packages',
                               dest='list',
                               action='store_true',
                               default=False,
                               help="list available packages (do not download)")
        self.parser.add_option('-f',
                               '--force',
                               dest='force',
                               action='store_true',
                               default=False,
                               help="force re-download all packages")
        self.parser.add_option('-V',
                               '--version',
                               dest='version',
                               action='store',
                               type='string',
                               default='current',
                               help="specify the Wazo version to build. Default is 'current'")

        (self.options, self.args) = self.parser.parse_args()
        self._validate_args()

    def _validate_args(self):
        if not self.options.list and len(self.args) != 1:
            self.parser.print_help()
            sys.exit(2)

    def _define_version(self):
        architecture = self._get_architecture()
        if self.options.version == 'current':
            self.release = 'debian'
            self.SUITES = [
                'wazo-dev-stretch/main/binary-%s/Packages' % architecture,
            ]
        elif self.options.version == 'rc':
            self.release = 'debian'
            self.SUITES = [
                'wazo-rc/main/binary-%s/Packages' % architecture,
            ]
        else:
            self.release = 'archive'
            if self.options.version < '13.25':
                distribution = 'squeeze-xivo-skaro-%s' % self.options.version
            elif self.options.version < '16.16':
                distribution = 'xivo-%s' % self.options.version
            else:
                distribution = 'wazo-%s' % self.options.version
            self.SUITES = [
                '%s/main/binary-%s/Packages' % (distribution, architecture),
            ]

    def _whitelist(self):
        self.include = [
            'xivo-dist'
        ]
        self.exclude = [
            'cracklib',
            'dahdi-linux-source',
            'libcrack2',
            'libctl',
            'libnet-ssh-ruby',
            'libruby',
            'meep', 'libmeep',
            'misdn-kernel-source',
            'mpb',
            'pf-sys-ssh',
            'pfbotnet', 'libpfbotnet',
            'python-cap',
            'python-crack',
            'sangoma-dbg',
            'sangoma-wanpipe-source',
            'squid',
            'swig',
            'tshark',
            'wireshark',
            'xivo-dev-ssh-pubkeys'
        ]
        self.skip = False

    def _list_packages(self):
        for src in self.SUITES:
            mirror_host = '%s/dists/%s' % (self.mirror, src)
            f = urllib2.urlopen(mirror_host)
            package_process = ''
            for line in f.readlines():
                if line.startswith('Package:'):
                    self.skip = True
                    package = line.split(' ')[1][:-1].strip()

                    if package not in self.include and \
                            (package.endswith('-dev') or
                             len(filter(lambda x: package.startswith(x), self.exclude)) > 0):
                        continue

                    self.skip = False

                if self.skip:
                    continue

                if package_process != package:
                    package_process = package
                    self.packages[package_process] = {}

                if line.startswith('Installed-Size:'):
                    self.stats['installed-size'] += int(line.split(' ')[1].strip())
                elif line.startswith('Size:'):
                    self.stats['size'] += int(line.split(' ')[1].strip())
                    self.packages[package_process]['Size'] = int(line.split(' ')[1].strip())
                elif line.startswith('Filename:'):
                    self.packages[package_process]['Filename'] = line.split(' ')[1].strip()
                elif line.startswith('MD5sum:'):
                    self.packages[package_process]['MD5sum'] = line.split(' ')[1].strip()

            f.close()

    def _print_list(self):
        for package, pkg_opts in self.packages.iteritems():
            print '%s: %s' % (package, pkg_opts['Filename'])
        print self.stats
        sys.exit(0)

    def _download_packages(self):
        if not os.path.exists(self.args[0]):
            os.makedirs(self.args[0])

        for package, pkg_opts in self.packages.iteritems():
            target = '%s/%s' % (self.mirror, pkg_opts['Filename'])
            debfilename = os.path.basename(target)
            local_debfile_path = os.path.join(self.args[0], debfilename)

            print 'Processing.. %s' % target
            if os.path.exists(local_debfile_path):
                md5sum = md5_checksum(local_debfile_path)
                if md5sum == pkg_opts['MD5sum']:
                    print ' . skipping... (MD5sum match)'
                    continue

            print " . downloading..."
            proc = subprocess.Popen(['wget', '-nv', '-P', self.args[0], target])
            proc.communicate()


def md5_checksum(fil_path):
    fh = open(fil_path, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


if __name__ == '__main__':
    main()
