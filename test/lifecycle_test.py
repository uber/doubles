from threading import Thread
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from doubles import lifecycle, expect, allow, clear
import doubles.testing


class TestLifecycle(object):
    def test_stores_a_space_per_thread(self):
        queue = Queue()

        def push_thread_space_to_queue(queue):
            queue.put(lifecycle.current_space())

        push_thread_space_to_queue(queue)

        thread = Thread(target=push_thread_space_to_queue, args=(queue,))
        thread.start()
        thread.join()

        main_space = queue.get()
        thread_space = queue.get()

        assert main_space is not thread_space


class TestClear(object):

    def test_does_not_raise_expectation_errors(self):
        expect(doubles.testing).top_level_function
        clear(doubles.testing)

    def test_new_allowances_can_be_set(self):
        (allow(doubles.testing).
            top_level_function.
            with_args('Bob Barker').
            and_return('Drew Carey'))

        clear(doubles.testing)
        allow(doubles.testing).top_level_function.and_return('Bob Barker')

        assert doubles.testing.top_level_function('bar') == 'Bob Barker'

    def test_clearing_an_instance(self):
        user = doubles.testing.User('Bob Barker', 25)
        (allow(user).
            method_with_positional_arguments.
            with_args(25).
            and_return('The price is right'))

        clear(user)
        allow(user).method_with_positional_arguments.and_return('The price is wrong')

        assert user.method_with_positional_arguments(10) == 'The price is wrong'

    def test_calling_twice(self):
        expect(doubles.testing).top_level_function
        clear(doubles.testing)
        clear(doubles.testing)

    def test_calling_on_an_undoubled_object(self):
        clear(doubles.testing)

        result = doubles.testing.top_level_function('bob')
        assert result == 'bob -- default'
