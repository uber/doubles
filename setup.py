from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

import doubles


with open('README.rst') as f:
    long_description = f.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='doubles',
    version=doubles.__version__,
    description='Test doubles for Python.',
    long_description=long_description,
    author='Jimmy Cuadra',
    author_email='jimmy@uber.com',
    url='https://github.com/uber/doubles',
    license='MIT',
    packages=['doubles', 'doubles.targets'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points = {
        'pytest11': ['doubles = doubles.pytest'],
        'nose.plugins.0.10': ['doubles = doubles.nose:NoseIntegration']
    },
    zip_safe=True,
    keywords=['testing', 'test doubles', 'mocks', 'mocking', 'stubs', 'stubbing'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
    ]
)
