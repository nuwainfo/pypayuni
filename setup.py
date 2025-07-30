# -*- coding: UTF-8 -*-
try:
    from setuptools import setup
except:
    from distutils.core import setup

__version__ = '0.1.2'
__author__ = 'Claire Chen'
__email__ = 'claire.chen@nuwainfo.com'

long_description = """
This is PayUni(統一金流) SDK implemented in Python.
Features:
Checkout a payment with following method:
- ATM
- WebATM
- CVS
- BARCODE
Dealing with the POST data after a payment is created or the customer pays.
Check out github repo: https://github.com/nuwainfo/pypayuni
"""

setup(
    name='pypayuni',
    version=__version__,
    author=__author__,
    author_email=__email__,
    packages=[
        'pypayuni',
    ],
    url='https://github.com/nuwainfo/pypayuni',
    license='LICENSE',
    description='PAYUNi API in python',
    long_description=long_description,
    install_requires=[
        "pycryptodome>=3.9.0", # For AES encryption
        "six>=1.11.0",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
