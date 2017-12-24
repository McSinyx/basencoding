===========
basencoding
===========

This package contains a Python 3 module and script for basencoding, which
treats each byte sequence as a base-256 number and convert it to another base
between 2 and 36.

basencoding (the module)
------------------------

This provide two functions ``encode(data, [base])`` and
``decode(data, [base, encoding])`` to encode and decode a ``bytes`` ``data``
using basencoding and return a ``bytes`` object.

The argument ``base`` is also a ``bytes`` and might be in either base-36 (to
specify output's case) or base-10 (and ``0`` for lower, ``1`` for upper 36).

Because the functions process ``bytes``, so they can deal with all kind of
data, text (encoded in any encoding support by Python), binary, etc. For
example::

  >>> encode(b'CnX', b'g')
  b'436e58\n'
  >>> decode(encode('Phần mềm tự do muôn năm!'.encode())).decode()
  'Phần mềm tự do muôn năm!'

basenc (the script)
-------------------

This is the front-end for ``basencoding``, which supports both Standard I/O and
files. Encoded output will be 1.5 to 8 times larger than the input data,
depending on the base chosen to encode. Note that the program is *incredibly*
slow on big data (100kB and above) as it converts the whole data scheme to one
integer.

::

  $ basenc -h
  usage: basenc [-h] [-v] [-i INFILE] [-o OUTFILE] [-d] [-b BASE] [-e ENCODING]

  Encode and decode files using basencoding.

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -i INFILE, --infile INFILE
                          input file, if not set read standard input
    -o OUTFILE, --outfile OUTFILE
                          output file, if not set read standard output
    -d, --decode          decode the data
    -b BASE, --base BASE  base system between 2 and 36, written in base 36 to
                          specify letters case of output if needed (incase base
                          is 36, use 0 for lowercase, 1 for uppercase). If this
                          is not set, the base will be picked to ensure data is
                          decodable to text in set encoding when decode, and
                          picked randomly when encode.
    -e ENCODING, --encoding ENCODING
                          set encoding, only useful when base is not set
                          
For example::

  $ echo 48656c6c6f2C20576f726C64210A | basenc -d
  Hello, World!
  $ basenc -i foobar
  56c5A920546869c3AA6e205472756e67204869e1Babf750A
  $ basenc -i /usr/bin/python3 -o base_python3 -b 20

If you find any bug or have any suggestion, please fill an issue on Github:
https://github.com/McSinyx/basencoding. Enjoy the encoding toy!
