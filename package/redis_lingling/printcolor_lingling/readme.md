## 说明

核心函数：

```
def print_testresult(*list):
```

说明：

* 显示结果有两种：【1】正确，显示（字符串 + ok）【2】错误（红色背景，字符串 + Error）；
* list形式是可变参数，至少2个参数，否则为错误；
* 最后一个参数必须是一个字符串；
* 之前的参数应当都是 True。如果有至少一个False；则为错误，其他情况为正确。