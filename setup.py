import re
from setuptools import setup, find_packages

with open('symbiflow/__init__.py', 'r') as f:
    version = re.search(r"__version__ = '([\d\.]*)'", f.read()).group(1)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='symbiflow',
    version=version,
    description='A CLI utility which solves HDL-to-bitstream based on FOSS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rodrigo A. Melo',
    author_email='rodrigomelo9@gmail.com',
    license='ISC',
    url='https://github.com/PyFPGA/symbiflow_cli',
    package_data={'': ['*.yml', 'templates/*']},
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'symbiflow = symbiflow.cli:main',
            'symbiconf = symbiflow.oci:main'
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ],
    install_requires=['pyyaml'],
    python_requires=">=3.6, <4"
)
