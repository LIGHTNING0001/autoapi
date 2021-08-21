import shutil

from setuptools import setup, find_packages
import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CUR_PATH, 'build')
if os.path.isdir(path):
    print('INFO del dir ', path)
    shutil.rmtree(path)

setup(
    name='apiauto',
    version='1.0',
    author='lishanjie',
    author_email='lishanjie914@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'xlrd'
    ],
)
