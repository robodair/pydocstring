import re
from os import path
import subprocess
from subprocess import CalledProcessError
from setuptools import find_packages, setup

INIT_FILE="pydocstring/__init__.py"
contents = open(INIT_FILE, "rt").read()
VS_RE = r"^__version__ = ['\"]([^'\"]*)['\"]"
version_attr = re.search(VS_RE, contents, re.M)
if version_attr:
    version = version_attr.group(1)
else:
    raise RuntimeError("Unable to find version string in {0}.".format(INIT_FILE))

classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: Plugins',
    'Environment :: Win32 (MS Windows)',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Documentation',
]

with open(path.join(path.dirname(__file__), "README.rst")) as readme_file:
    long_description = readme_file.read()

setup(
    name='pydocstring',
    version=version,
    url='https://github.com/robodair/pydocstring',
    author='Alisdair Robertson',
    author_email='alisdair.w.robertson@gmail.com',
    description='Package providing autocompletion capabilities for python docstrings',
    long_description=long_description,
    license='MIT',
    packages=find_packages(exclude=('tests')),
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'pydocstring=pydocstring.cli:main',
        ],
    },
    install_requires=[
        'parso>=0.1.1'
    ]
)
