from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kerasplugins',

    version='0.1.3',

    description='Keras Plugins',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mainanick/kerasplugins',

    # Author details
    author='Nick Maina',
    author_email='nick.maina1@gmail.com',

    license='MIT',

    classifiers=[

        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',

        'Natural Language :: English',

        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='keras',

    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=[
        'keras',
        'requests',
        'telegram',
        'slacker'
    ],
)
