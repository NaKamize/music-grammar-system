from setuptools import setup, find_packages

setup(
    name='multigenerative-grammar-cli',
    version='0.1.0',
    description='A command line application that implements a multigenerative grammar system with scattered context grammars to parse grammar examples and produce MIDI music files.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
        'mido',  # Example dependency for MIDI file handling
        'some-grammar-library',  # Replace with actual grammar parsing library
    ],
    entry_points={
        'console_scripts': [
            'multigenerative-grammar=main:main',  # Adjust the entry point as necessary
        ],
    },
)