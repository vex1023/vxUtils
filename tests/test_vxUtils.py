# encoding = utf-8
'''
测试用例
'''
import time
import unittest

from vxUtils.decorator import threads, timeout, timeit, retry


@threads(3)
def hello(n):
    print('start to sleep')
    time.sleep(1)
    print('sleep 1 seconds: %s' % n)
    return n



class MyTestCase(unittest.TestCase):
    def test_threads(self):
        print('start testing')
        a = [hello(n) for n in range(10)]
        print('end testing')
        [print(i.result) for i in a]

    def test_timeout(self):
        print('start testing timeout')

        @timeout(2)
        def test():
            time.sleep(6)
            return 'hello world'

        try:
            test()
        except TimeoutError as err:
            self.assertIsInstance(err, TimeoutError)

        return

    def test_timeit(self):

        @timeit
        def test1():
            time.sleep(1)

        test1()

    def test_retry(self):

        @retry(5, AssertionError)
        def test2():
            pass

if __name__ == '__main__':
    unittest.main()
