from setuptools import setup, find_packages

setup(

    # this will be my Library name.
    name='td-ameritrade-python-gym',

    # Want to make sure people know who made it.
    author='Joshua M. Stevens',

    # also an email they can use to reach out.
    author_email='joshua.stevens@obolary.com',

    # I'm in alpha development still, so a compliant version number is a1.
    # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
    version='0.1.0',

    # here is a simple description of the library, this will appear when
    # someone searches for the library on https://pypi.org/search
    description='A python library for OpenAI gym based interface to td-ameritrade APIs',

    # here is the URL you can find the code, this is just the GitHub URL.
    url='https://github.com/obolary/td-ameritrade-python-gym',

    # there are some dependencies to use the library, so let's list them out.
    install_requires=[ 'gym' ],

    # some keywords for my library.
    keywords='finance, gym',

    # here are the packages I want "build."
    packages=find_packages( include=[ 'td_gym' ] ),

    # you will need python 3.7 to use this libary.
    python_requires='>=3.7'
)
