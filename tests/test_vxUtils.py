# encoding = utf-8
'''
测试用例
'''
import unittest
import time
from vxUtils.decorator import threads

@threads(3)
def hello(n):
    print('start to sleep')
    time.sleep(1)
    print('sleep 1 seconds: %s' % n)
    return n



class MyTestCase(unittest.TestCase):
    def test_something(self):
        print('start testing')
        a = [hello(n) for n in range(10)]
        print('end testing')
        [print(i.result) for i in a]


        #self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
