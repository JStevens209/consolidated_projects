from setuptools import setup, find_packages

setup(

    # this will be my Library name.
    name='option-pricing-python',

    # Want to make sure people know who made it.
    author='Davis W. Edwards',

    # also an email they can use to reach out.
    author_email='davis.edwards@understandtrading.com',

    # I'm in alpha development still, so a compliant version number is a1.
    # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
    version='0.1.0',

    # here is a simple description of the library, this will appear when
    # someone searches for the library on https://pypi.org/search
    description='A libary to price financial options using closed-form solutions written in Python.',

    # want to make sure that I specify the long description as MARKDOWN.
    long_description_content_type="text/markdown",

    # here is the URL you can find the code, this is just the GitHub URL.
    url='https://github.com/obolary/option-pricing-python',

    # there are some dependencies to use the library, so let's list them out.
    install_requires=[],

    # some keywords for my library.
    keywords='finance, options',

    # here are the packages I want "build."
    packages=find_packages(include=['option_pricing']),

    # you will need python 3.7 to use this libary.
    python_requires='>=3.7'
)
