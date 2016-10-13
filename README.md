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


