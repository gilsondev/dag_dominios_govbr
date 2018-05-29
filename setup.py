#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
import shutil

from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

DAG_FILE = 'dag_dominios_govbr.py'
DAG_FILE_PATH = Path(f'./dag_dominios_govbr/{DAG_FILE}')

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
DAGS_FOLDER_PATH = Path(f'{AIRFLOW_HOME}/dags/{DAG_FILE}')


def _copy_dag_file(symlink=False):
    if symlink:
        os.symlink(DAG_FILE_PATH.absolute(), DAGS_FOLDER_PATH)
    else:
        shutil.copy(DAG_FILE_PATH, DAGS_FOLDER_PATH)


class PostDevelopCommand(develop):
    def run(self):
        _copy_dag_file(symlink=True)
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        _copy_dag_file()
        install.run(self)


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest',
    'responses',
]

setup(
    author="Gilson Filho",
    author_email='me@gilsondev.in',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Projeto criado para importar dados dos dominios gov.br autorizados pelo Min. do Planejamento",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dag_dominios_govbr',
    name='dag_dominios_govbr',
    packages=find_packages(include=['dag_dominios_govbr']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gilsondev/dag_dominios_govbr',
    version='0.1.0',
    zip_safe=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    },
)
