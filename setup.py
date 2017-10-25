import re
from os import path
import subprocess
from subprocess import CalledProcessError
from setuptools import find_packages, setup

VERSIONFILE="pydocstring/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: Plugins',
    'Environment :: Win32 (MS Windows)',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
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
        'parso==0.1.1'
    ],
    extras_require = {
        "dev": [
            "nose==1.3.7",
            "coverage==4.4.1",
            "rednose==1.2.2",
            "Sphinx==1.6.3",
            "pylint==1.7.2",
            "sphinx_rtd_theme==0.2.4",
            "sphinxcontrib-napoleon==0.6.1",
            "twine==1.9.1",
            "tox==2.9.1",
            "pytest==3.2.5"
        ]
    }
)
