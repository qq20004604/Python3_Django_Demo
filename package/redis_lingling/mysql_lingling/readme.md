# 说明

安装：

```bash
pip install mysql-connector
```

## 1、作用

``mysql`` 模块的再包装，并支持 with语法。

将使用简化抽象为：

1. 连接数据库；
2. 执行sql语句并获得返回结果；
3. 关闭数据库（使用with的时候可以省略）；

## 2、示例

示例1（with语法）

```
# 连接数据库
with MySQLTool(user=user, password=pw, database=database) as m2:
    # 执行sql并获得返回结果
    result2 = m2.run_sql([
        ['insert person(name, age) values ("李四", 20), ("王五", 30)'],
        ['select * from person']
    ])
    # 打印结果
    print(result2)
```

示例2（普通语法）

```
m = MySQLTool()
# 查看mysql容器内 ip，参考这个链接：https://blog.csdn.net/CSDN_duomaomao/article/details/75638544
m.connect(user=user,
          password=pw,
          # host=ip,
          database=database)
result = m.run_sql([
    ['insert person(name,age) values (%s, %s)', ['六六六', 666]],
    ['select * from person']
])
print(result)
m.close()
```