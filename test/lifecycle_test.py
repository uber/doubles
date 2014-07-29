from threading import Thread
from Queue import Queue

from doubles import lifecycle


class TestLifecycle(object):
    def test_stores_a_space_per_thread(self):
        queue = Queue()

        queue.put(lifecycle.current_space())

        def push_thread_space_to_queue(queue):
            queue.put(lifecycle.current_space())

        thread = Thread(target=push_thread_space_to_queue, args=(queue,))
        thread.start()
        thread.join()

        main_space = queue.get()
        thread_space = queue.get()

        assert main_space is not thread_space
