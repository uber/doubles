pytest_plugins = "pytester"


def test_exceptions_dont_cause_leaking_between_tests(testdir, capsys):
    testdir.makepyfile("""

        from doubles.targets.expectation_target import expect
        from doubles.testing import User

        def test_that_sets_expectation_then_raises():
            expect(User).class_method.with_args(1).once()
            raise Exception('Bob')

        def test_that_should_pass():
            assert True

    """)
    result = testdir.runpytest()
    outcomes = result.parseoutcomes()
    assert outcomes['failed'] == 1
    assert outcomes['passed'] == 1


def test_failed_expections_do_not_leak_between_tests(testdir, capsys):
    testdir.makepyfile("""

        from doubles.targets.expectation_target import expect
        from doubles.testing import User

        def test_that_fails_for_not_satisfying_expectation():
            expect(User).class_method.with_args(1).once()

        def test_that_should_fail_for_not_satisfying_expection():
            expect(User).class_method.with_args('bob').once()

    """)
    result = testdir.runpytest()
    outcomes = result.parseoutcomes()
    assert outcomes['failed'] == 2
