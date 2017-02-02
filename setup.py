#!/usr/bin/env python3

from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name='basencoding',
      version='0.1.0a1',
      url='https://github.com/McSinyx/basencoding',
      description='convert byte sequence to integer in multiple bases',
      long_description=long_description,
      author='Raphael McSinyx',
      author_email='vn.mcsinyx@gmail.com',
      license='GPLv3+',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Other Audience',
          'License :: OSI Approved :: GNU General Public License v3 or later'
          +' (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Security :: Cryptography',
      ],
      keywords='encoding encription',
      py_modules=['basencoding'],
      scripts=['basenc'],
      )
