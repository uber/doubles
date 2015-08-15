from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

with open('README.rst') as f:
    long_description = f.read()

if sys.version_info < (3,2):
    install_requires = ['futures']
else:
    install_requires = []


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
    version='1.0.8',
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
    ],
    install_requires = install_requires,
)
