# Redis说明

## 1、Redis是什么？优势？不同？

参考菜鸟教程。

【是什么？】

REmote DIctionary Server(Redis) 是一个由Salvatore Sanfilippo写的key-value存储系统。

Redis是一个开源的使用ANSI C语言编写、遵守BSD协议、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。

它通常被称为数据结构服务器，因为值（value）可以是 字符串(String), 哈希(Hash), 列表(list), 集合(sets) 和 有序集合(sorted sets)等类型。

Redis 是完全开源免费的，遵守BSD协议，是一个高性能的key-value数据库。

Redis 与其他 key - value 缓存产品有以下三个特点：

* Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
* Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
* Redis支持数据的备份，即master-slave模式的数据备份。


【优势】

* 性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
* 丰富的数据类型 – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作。
原子 – Redis的所有操作都是原子性的，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过MULTI和EXEC指令包起来。
* 丰富的特性 – Redis还支持 publish/subscribe, 通知, key 过期等等特性。

【不同】

* Redis有着更为复杂的数据结构并且提供对他们的原子性操作，这是一个不同于其他数据库的进化路径。Redis的数据类型都是基于基本数据结构的同时对程序员透明，无需进行额外的抽象。

* Redis运行在内存中但是可以持久化到磁盘，所以在对不同数据集进行高速读写时需要权衡内存，因为数据量不能大于硬件内存。在内存数据库方面的另一个优点是，相比在磁盘上相同的复杂的数据结构，在内存中操作起来非常简单，这样Redis可以做很多内部复杂性很强的事情。同时，在磁盘格式方面他们是紧凑的以追加的方式产生的，因为他们并不需要进行随机访问。

## 2、安装

特指Linux。

先打开 http://download.redis.io/releases/ 查看最新版的 Redis的版本。

然后执行（5.0.4是版本号）将资源下载到本地

```
wget http://download.redis.io/releases/redis-5.0.4.tar.gz
```

解压缩然后安装：

```
tar xzf redis-5.0.4.tar.gz
cd redis-5.0.4
make
```

安装完后，会提示你执行 ``make test`` 进行测试。

此时有可能会提示你 tcl 版本太低

```
You need tcl 8.5 or newer in order to run the Redis test
```

那么执行以下代码：

```
wget https://prdownloads.sourceforge.net/tcl/tcl8.6.9-src.tar.gz
tar xzvf tcl8.6.1-src.tar.gz
cd  tcl8.6.1-src/unix
./configure
make
make install 
```

如果提示权限问题就加 sudo

## 3、运行

在 redis 根目录下，进入 src 文件夹，并运行 ``redis-server``

```
cd src
./redis-server
```

运行成功（注意，此时是前台执行），当前tab不可用。

再开一个ssh链接，到同目录下，执行

```
./redis-cli
```

如下：

```
[root@localhost src]# ./redis-cli 
127.0.0.1:6379> 
```

说明可用。

输入 ``set foo a``，设置key和value，再输入 ``get foo`` 来获取值，如下

```
127.0.0.1:6379> set foo a
OK
127.0.0.1:6379> get foo
"a"
```

说明一切OK。

## 4、远程连接

使用 Python 来实现远程连接。

### 4.1、先安装 Python 的 redis

```
pip install redis
```

### 4.2、编辑 Python 连接 Redis 的代码

如下写代码：

```
import redis

# host是redis主机，需要启动 ./redis-server
# redis默认port（端口）是6379
# decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
# password 需要密码。非同机访问，需要填写密码才可以访问
r = redis.Redis(host='192.168.0.104', port=6379, decode_responses=True, password='fsdfwef32r23r32vsdvvavsfdvsf12e21fav')
# key是"foo" value是"bar" 将键值对存入redis缓存
r.set('foo', 'is foo')
# 取出键foo对应的值，这两种方式都可以
print(r['foo'])
print(r.get('foo'))
```

### 4.3、配置Redis

这个时候我们会遇见一些问题。

第一个问题，直接运行以上代码，Python会等待一会（没有返回信息），然后报错，告知说连接不上。

这是因为要配置 redis，允许远程连接。

打开根目录下的 ``redis.conf`` 文件。


#### 4.3.1、bind配置

首先编辑 bind 配置。如以下（已添加中文注释）

```
################################## NETWORK #####################################

# By default, if no "bind" configuration directive is specified, Redis listens
# for connections from all the network interfaces available on the server.
# It is possible to listen to just one or multiple selected interfaces using
# the "bind" configuration directive, followed by one or more IP addresses.
#
# 默认情况下，如果没有指定bind配置，redis 将监听服务器允许的所有网络的接口。
# 将根据一个或多个IP地址，允许监听一个或多个已选择接口使用bind配置
# Examples:
#
# bind 192.168.1.100 10.0.0.1
# bind 127.0.0.1 ::1
#
# ~~~ WARNING ~~~ If the computer running Redis is directly exposed to the
# internet, binding to all the interfaces is dangerous and will expose the
# instance to everybody on the internet. So by default we uncomment the
# following bind directive, that will force Redis to listen only into
# the IPv4 loopback interface address (this means Redis will be able to
# accept connections only from clients running into the same computer it
# is running).
# ~~~警告~~~如果运行redis的服务器并且直接暴露给网络，绑定了所有网络接口，
# 这是一个危险的行为，并且将导致每个来自互联网的用户都可以访问接口。
# 所以，默认情况下，我们取消以上关于直接绑定IP的注释，这会强制redis只监听
# IPv4 回传的接口地址（这意味着，redis将只允许接受来自于相同电脑上运行的
# 客户端的连接）
# 【译者注】总结一下：如果没有任何bind绑定，那么任何电脑都能访问。
# 如果加了bind绑定，如 bind 127.0.0.1。那么只允许相同电脑上的redis客户端访问。
# 这里的bind绑定的IP，指 redis 自身的IP（本机IP、内网IP、外网IP），
# 而不是指访问者的IP。如果允许内网或外网访问，需要添加密码（修改下面的SECURITY）
#　
# IF YOU ARE SURE YOU WANT YOUR INSTANCE TO LISTEN TO ALL THE INTERFACES
# JUST COMMENT THE FOLLOWING LINE.
# 【如果，你确认你想要你的服务器监听所有的网络接口，那么注释掉下面这行线）
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bind 127.0.0.1 192.168.0.104
```

简单来说，这个配置分为多种情况：

* 没有配置，那么将默认允许本机、外网和内网的其他服务器访问 Redis 服务器；
* 配置为：``bind 127.0.0.1``，将只允许本机访问；
* 配置为：``bind 127.0.0.1 [内网IP]`` 将允许本机和内网访问，这里的内网IP，指 Redis 服务器的内网IP，而不是指访问者的；
* 配置为：``bind 127.0.0.1 [外网IP]`` 将允许本机和外网访问，同样，外网IP 指 Redis 服务器的外网IP；
* 当然，也可以同时设置 内网IP 和 外网IP；

唯一需要注意的是，这里限制的 IP，都是指 Redis 在内网、外网的IP，而不是访问者的。可以通过 ifconfig　来获取本机的ip地址；

#### 4.3.2、配置Auth

因为允许都访问了，所以就存在安全问题，需要设置 Auth（授权，也可以理解为密码）。

同样是编辑 ``redis.conf`` 文件，代码如下：

```
################################## SECURITY ###################################
# 安全
# Require clients to issue AUTH <PASSWORD> before processing any other
# commands.  This might be useful in environments in which you do not trust
# others with access to the host running redis-server.
# 在处理任何命令之前，需要客户端提交 授权<密码>。
# 这在你处于一个不相信任何连接redis主机的其他主机的环境中时，非常有帮助。
#
# This should stay commented out for backward compatibility and because most
# people do not need auth (e.g. they run their own servers).
# 为了向后兼容，应保留注释，因为很多人并不需要 授权（因为他们跑在他们自己的服务器上）
#
# Warning: since Redis is pretty fast an outside user can try up to
# 150k passwords per second against a good box. This means that you should
# use a very strong password otherwise it will be very easy to break.
# 警告：自从 redis 变得非常快之后，外部用户可以通过每秒超过15w次用密码来尝试破解。
# 这意味着，你需要使用一个非常非常长的密码，否则他（redis）的密码将会很容易被破解。
#
# requirepass foobared
# 这里按格式写密码：requirepass 你的密码
requirepass fsdfwef32r23r32vsdvvavsfdvsf12e21fav
# 密码是 fsdfwef32r23r32vsdvvavsfdvsf12e21fav
```

参考注释里的翻译。


#### 4.4、验证

这个时候，运行以上python代码，可以正确打印出数据了。