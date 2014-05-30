from setuptools import setup

import doubles

setup(
    name='doubles',
    version=doubles.__version__,
    description='Test doubles for Python.',
    author='Jimmy Cuadra',
    author_email='jimmy@uber.com',
    url='https://github.com/uber/doubles',
    license='MIT',
    packages=['doubles'],
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
    ]
)
