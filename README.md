# vxUtils

这是我的工具箱


## decorator 修饰器

1.  retry

错误重试的修饰器

```python
from vxUtils.decorator import retry

@retry(5, ValueError, delay=1, backoff=2)
def test():

    raise ValueError('try it ')
```

2.  timeit

计算运行消耗时间

```python
import time
from vxUtils.decorator import timeit

@timeit
def test():
    time.sleep(5)
```

3. Singleton

设计模式：单例实现方式

```python
from vxUtils.decorator import singleton

@singleton
class Test():
    pass
```

4.  threads

异步多线程

```python
import requests
from vxUtils.decorator import threads

@threads(5)
def get_url(url):
    return requests.get(url)

if __name__ == '__main__':
    urls = [
        'www.sina.com',
        'www.baidu.com',
        'www.qq.com',
        'www.taobao.com'
    ]
    
    responses = [get_url(url) for url in urls]
    for r in responses:
        print(r.content)
        
```

5. timeout

限制超时时间

```python
import time
from vxUtils.decorator import timeout

@timeout(5)
def test():
    print('start to test')
    for n in range(10):
        time.sleep(1)
        print('n: %s' % n)
```

## PrettyLogger

漂亮的日志格式

1.  add_console_logger

增加console logger

```python
import logging
from vxUtils.PrettyLogger import add_console_logger

logger = logging.getLogger('test')

logger = add_console_logger(logger, 'debug')

logger.debug('蓝色') 
logger.info('绿色')
logger.warnning('黄色')
logger.error('棕色')
logger.critical('红色')
```

2. add_qyWechat_logger

企业微信号,日志通知

```python
import logging
from vxUtils.PrettyLogger import add_qyWechat_logger

logger = logging.getLogger('test')

logger = add_qyWechat_logger(logger,'warning',corpid, appsecret, agentid)

logger.warning('这是微信日志通知')
```