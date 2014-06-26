# doubles

**Doubles** is a Python package that provides test doubles for use in automated tests.

It provides functionality for stubbing, mocking, and verification of test doubles against the real objects they double. In contrast to the Mock package, it provides a clear, expressive syntax and better safety guarantees to prevent API drift and to improve confidence in tests using doubles.

## Documentation

Documentation is available at http://doubles.readthedocs.org/en/latest/.

## Development

Source code is available at https://github.com/uber/doubles.

To install the dependencies on a fresh clone of the repository, run `make bootstrap`.

To run the full test suite, run `./run_tests.sh`.

To run just the test suite for Doubles itself, run `make test`.

To run the test suite for unittest integration, run `make unittest`. (The suite is expected to fail.)

To build the documentation locally, run `make docs`.

## License

[MIT](http://opensource.org/licenses/MIT)
