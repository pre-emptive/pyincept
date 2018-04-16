from distutils.core import setup
import glob
import os

data_files = []
for root, dirs, files in os.walk("incept/skel/"):
    path = root.split(os.sep)
    #print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        #print(len(path) * '---', file)
        data_files.append("%s%s%s" %( root, os.sep, file))

print "data_files = %s" % (data_files)

setup(
    name='pyincept',
    url='https://github.com/pre-emptive/pyincept',
    author='Ralph Bolton',
    author_email='devnull@coofercat.com',
    version='1.0.7',
    packages=['incept'],
    scripts=['scripts/incept'],
    package_data={'incept': ['skel/*/*','skel/*/.exists'] },
    license='GPLv2',
    long_description=open('README.md').read(),
)
