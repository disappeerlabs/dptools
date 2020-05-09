from setuptools import setup, find_packages
from dptools import metainfo


setup(
    name=metainfo.title,
    version=metainfo.version,
    description='Tools library for components and subsystems in the Disappeer project',
    author='Disappeer Labs',
    author_email=metainfo.email,
    license='GPLv3',
    packages=find_packages(exclude=('tests',)),
)
