# endcoding = utf-8
'''
author : vex1023
email :  vex1023@qq.com

各类型的decorator
'''

import logging
import signal
import time
from multiprocessing.pool import ThreadPool

from functools import wraps

from . import __logger__

logname = '.'.join([__logger__, 'decorator'])

logger = logging.getLogger('vex1023')


###################################
# 错误重试方法实现
# @retry(tries, CatchExceptions=(Exception,), delay=0.01, backoff=2)
###################################
def retry(tries, CatchExceptions=(Exception,), delay=0.01, backoff=2):
    '''
    错误重试的修饰器
    :param tries: 重试次数
    :param CatchExceptions: 需要重试的exception列表
    :param delay: 重试前等待
    :param backoff: 重试n次后，需要等待delay * n * backoff
    :return:


    @retry(5,ValueError)
    def test():
        raise ValueError

    '''
    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")

    if tries < 0:
        raise ValueError("tries must be 0 or greater")

    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mdelay = delay
            retException = None
            for mtries in range(tries):
                try:
                    return f(*args, **kwargs)
                except CatchExceptions as ex:
                    logger.warning(
                        "function %s(%s, %s) try %d times error: %s\n" % (f.__name__, args, kwargs, mtries, str(ex)))
                    logger.warning("Retrying in %.4f seconds..." % (mdelay))

                    retException = ex
                    time.sleep(mdelay)
                    mdelay *= backoff
            raise retException

        return f_retry

    return deco_retry


###################################
# 计算运行消耗时间
# @timeit
###################################
def timeit(func):
    '''
    计算运行消耗时间
    @timeit
    def test():
        time.sleep(1)
    '''

    def wapper(*args, **kwargs):
        _start = time.time()
        retval = func(*args, **kwargs)
        _end = time.time()
        logger.info('function %s() used : %.6f s' % (func.__name__, _end - _start))
        return retval

    return wapper


###################################
# Singleton 实现
# @singleton
###################################
def singleton(cls):
    '''
    单例实现
    @singleton
    class test():
        pass
    '''

    cls.__new_original__ = cls.__new__

    @wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


###################################
# 异步多线程
# @thread(n,timeout=None)
###################################

class asyncResult():
    def __init__(self, future, timeout):
        self._future = future
        self._timeout = timeout

    def __getattr__(self, name):
        result = self._wait()
        return result.__getattribute__(name)

    @property
    def result(self):
        return self._wait()

    def _wait(self):
        return self._future.get(self._timeout)


def threads(n, timeout=5):
    def decorator(f):
        pool = ThreadPool(n)

        @wraps(f)
        def warpped(*args, **kwargs):
            return asyncResult(
                pool.apply_async(func=f, args=args, kwds=kwargs),
                timeout
            )

        return warpped

    return decorator


###################################
# 限制超时时间
# @timeout(seconds, error_message='Function call timed out')
###################################

def timeout(seconds, error_message='Function call timed out'):
    def decorated(func):
        def _handle_timeout(signum, frame):
            logger.warning(error_message)
            raise TimeoutError(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorated
