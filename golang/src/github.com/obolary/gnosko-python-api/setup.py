from setuptools import setup, find_packages

setup(

    # this will be my Library name.
    name='gnosko-python-api',

    # Want to make sure people know who made it.
    author='Ira Stevens',

    # also an email they can use to reach out.
    author_email='support@obolary.com',

    # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
    version='0.1.0',

    # here is a simple description of the library, this will appear when
    # someone searches for the library on https://pypi.org/search
    description='A python client lirbary for the Gnosko API.',

    # there are some dependencies to use the library, so let's list them out.
    install_requires=[
        'requests'
    ],

    # some keywords for my library.
    keywords='finance, gnosko, api',

    # here are the packages I want "build."
    packages=find_packages(include=['gnosko']),

    # you will need python 3.7 to use this libary.
    python_requires='>=3.7'

)
