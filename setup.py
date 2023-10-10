import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

with open('README.rst') as f:
    long_description = f.read()

with open('dobles/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='dobles',
      version=version,
      description='Test dobles for Python.',
      long_description=long_description,
      author='Jimmy Cuadra',
      author_email='jimmy@uber.com',
      url='https://github.com/uber/dobles',
      license='MIT',
      packages=['dobles', 'dobles.targets'],
      install_requires=['six'],
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      entry_points={
          'pytest11': ['dobles = dobles.pytest_plugin'],
      },
      zip_safe=True,
      keywords=[
          'testing', 'test dobles', 'mocks', 'mocking', 'stubs', 'stubbing'
      ],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Testing',
      ])
