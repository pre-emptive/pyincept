#from distutils.core import setup
from setuptools import setup,find_packages
import glob
import os

data_files = []
for root, dirs, files in os.walk("incept/skel/"):
    path = root.split(os.sep)
    for file in files:
        data_files.append("%s%s%s" %( root, os.sep, file))

setup(
    name='pyincept',
    url='https://github.com/pre-emptive/pyincept',
    author='Ralph Bolton',
    author_email='devnull@coofercat.com',
    version='1.0.13',
    packages=['incept'],
    entry_points={
        'console_scripts': [
            'incept=incept.__main__:main'
        ]
    },
    package_data={'incept': ['skel/*/*','skel/*/.exists'] },
    license='GPLv2',
    long_description=open('README.md').read(),
)
