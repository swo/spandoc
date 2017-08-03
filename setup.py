from __future__ import print_function
from setuptools import setup

setup(
    name='Spandoc',
    version='0.1',
    url='url',
    license='MIT',
    author='Scott Olesen',
    author_email='swo@alum.mit.edu',
    tests_require=['pytest'],
    install_requires=[
        'watchdog',
        ],
    description='Smarter Pandoc',
    long_description='Guess file inputs and outputs for pandoc',
    packages=['spandoc'],
    scripts=['scripts/spandoc.py']
)
