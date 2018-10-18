Changelog
=========

1.5.3 (2018-10-18)
----------------

- Add six library to install_requires

1.5.2 (2018-10-12)
----------------

- Add support for inspect.signature
- Add support of Python 3.7
- Fix inspect DeprecationWarning

1.5.1 (2018-7-24)
----------------

- Fix bug which breaks automatic teardown of top-level expectations between test cases

1.5.0 (2018-6-07)
----------------

- Report unsatisfied expectations as failures instead of errors.

1.4.0 (2018-4-25)
----------------

- Fix bug in unsatisfied `with_args_validator` exceptions.  Note this may cause some tests being run with the `unittest`
runner that used to pass to fail.

1.3.2 (2018-4-17)
----------------

- Fix bug in `and_raise`

1.3.1 (2018-4-16)
----------------

- Support Pytest 3.5
- Support Exceptions with custom args
- Cleanup test runner integration docs
- Update is_class check, use builtin method
- Cleanup some grammar in failure messages

1.2.1 (2016-3-20)
----------------

- Make expectation failure messages clearer

1.2.0 (2016-3-2)
----------------

- update pytest integration for version >=2.8
- Support arbitrary callables on class

1.1.3 (2015-10-3)
-----------------

- Fix bug when restoring stubbed attributes.

1.1.2 (2015-10-3)
-----------------

- Support stubbing callable attributes.

1.1.1 (2015-9-23)
-----------------

- Optimized suite by using a faster method of retrieving stack frames.

1.1.0 (2015-8-23)
-----------------

- Native support for futures: `and_return_future` and `and_raise_future`

1.0.8 (2015-3-31)
-----------------

- Allow with_args_validator to work with expectations

1.0.7 (2015-3-17)
-----------------

- Added __name__ and __doc__ proxying to ProxyMethod objects.
- Expectations can return values and raise exceptions.
- Add with_args_validator, user_defined arg validators.
- Validate arguments of a subset builtin objects (dict, tuple, list, set).
- Update FAQ.

1.0.6 (2015-02-16)
------------------

- Add with_args short hand syntax
- Improve argument verification for mock.ANY and equals
- Fix pep issues that were added to flake8

1.0.5 (2015-01-29)
------------------

- Started tracking changes
- Add expect_constructor and allow_constructor
- Add patch and patch_class
- Add clear
- Clarify some error messages
