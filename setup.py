#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import distutils
import platform
from setuptools import setup, find_packages

major, minor, micro = platform.python_version().split('.')

if major != '2' or minor not in ['6', '7']:
    raise Exception('unsupported version of python')

requires = ['pika == 0.9.5-1',
            'netifaces >= 0.5',
            'M2Crypto >= 0.15']

synapse_version = "Undefined"

try:
    import synapse.version as version_mod
    if version_mod.VERSION:
        synapse_version = version_mod.VERSION
except (ImportError, AttributeError):
    pass

data_files = [('/etc/synapse-agent', ['conf/synapse-agent.conf',
                                      'conf/logger.conf',
                                      'conf/permissions.conf']),
              ('/etc/synapse-agent/ssl', []),
              ('/etc/synapse-agent/ssl/private', []),
              ('/etc/synapse-agent/ssl/certs', []),
              ('/etc/synapse-agent/ssl/csr', []),
              ('/etc/init.d', ['scripts/synapse-agent']),
              ('/var/lib/synapse-agent/persistence', []),
              ('/var/log/synapse-agent', [])]

if platform.system().lower() == 'windows':
    win_data_files = []
    prefix = os.path.dirname(distutils.sysconfig.PREFIX)
    full_prefix = os.path.join(prefix, 'synapse-agent')

    for index, pair in enumerate(data_files):
        folder = pair[0].replace("/", "\\")[1:]
        flist = [x.replace("/", "\\") for x in pair[1]]
        win_data_files.append((os.path.join(full_prefix, folder), flist))

    data_files = win_data_files

scripts = ["bin/synapse-agent"]
dependency_links = ['http://github.com/raphdg/pika/tarball/ssl#egg=pika-0.9.5-1']

setup(
    name='synapse-agent',
    version=synapse_version,
    description='distribution-agnostic host management',
    author='Raphaël De Giusti',
    author_email='raphael.degiusti@gmail.com',
    url='https://github.com/comodit/synapse-agent',
    license='MIT License',
    packages=find_packages(),
    package_data={'': ['LICENSE', 'AUTHORS']},
    scripts=scripts,
    dependency_links=dependency_links,
    include_package_data=True,
    data_files=data_files,
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'License :: License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Content Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=requires,
)
