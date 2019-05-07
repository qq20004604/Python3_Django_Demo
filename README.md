# Python3_Django_Demo

## 0、说明

群主的QQ群：387017550

点击链接加入群聊【前端与后端交流学习】：https://jq.qq.com/?_wv=1027&k=53jrCzq

项目demo地址：https://github.com/qq20004604/Python3_Django_Demo

版本：

```
django版本：2.2.1
python版本：3.7
```

## 1、安装

```
pip3 install django
```

**初始化：**

直接用 pycharm 新建 django 项目。

或者输入命令行：

```
django-admin startproject [项目名]
```

会创建文件夹，并且文件夹内部有一个 文件夹（名字是项目名）。

例如：

```
django-admin startproject  
```

会在当前目录下创建一个 ``blogproject`` 文件夹，进入该文件夹后，还会有一个 ``blogproject`` 文件夹，这个里面有多个 py 文件，例如 ``urls.py``

## 2、创建新应用

**作用：**

同一个django项目下，可以有多个应用，互相之间独立，方便管理。

**创建：**

```
python manage.py startapp [项目名]
```

**效果：**

* 会在根目录（manage.py）下创建一个文件夹，名字等于 ``[项目名]``；
* 此时还需要引入到项目中；

**引入：**

假如新建的项目名是：``homepage``，初始化的django项目名是 demo

打开 ``/demo/urls.py`` 文件，添加内容，结果应该如下：

```python
from django.contrib import admin
from django.urls import path
# 引入项目
from homepage import views as homepage_views

# 这里配置 url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_views.index),
]
```

效果是 打开 ``/`` 路径，显示 ``homepage/views.py`` 里面设置的内容。

此时还需要编辑一下 ``homepage/views.py`` ，内容如下：

```
def index(request):
    return HttpResponse('Home Page')
```

下来启动项目进行验证。

看到这里，我默认你已经明白了如何添加一个新的 url 和 view 了。

## 3、启动项目

项目根目录下运行

```
python manage.py runserver 127.0.0.1:8000
```

打开页面：``http://127.0.0.1:8000/``，显示内容为：``Home Page``

注意，此时为【热更新项目】，即你修改后，不需要重启服务器，即时生效。

## 4、返回 html 文件

template 文件夹下新建 ``index.html``，内容：

```python
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>test</title>
</head>
<body>
Home Page Test
</body>
</html>
```

修改 ``homepage/views.py`` 如下：

```python
from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')
```

继续访问 ``http://127.0.0.1:8000/`` ，显示内容：``Home Page Test``

注意，此时页面和之前最大不同不是显示的内容不同，而是一个返回的是字符串，另一方返回的是 html 文件（从chrome的network可得知）。

**说明：**

1. 默认是只能取 templates 目录下的 html 文件；
2. 如果要取其他目录下的 html 文件，通过相对路径来写，默认是不可行的；
3. 推荐在 templates 目录下再建目录，比如 ``templates/homepage/xxx.html`` 这种形式来读取模板文件；
4. 优点是方便管理；
6. 另一个方法是通过改 ``项目名/settings.py``　的配置（缺点是复杂项目中，命中错误，后续和之前的文件名是一样）；

**修改settings.py`` 配置：**

如下：

```python
# 说明参考这个https://blog.csdn.net/xys430381_1/article/details/77943434
TEMPLATES = [
    {
        # BACKEND：模板引擎类的python路径，内置的模板引擎分别有'django.template.backends.django.DjangoTemplates'和'django.template.backends.jinja2.Jinja2'
        # DTL和jinja2的区别：https://www.atjiang.com/2scoopsdjango1.8-15-django-templates-and-jinja2/
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # render 的时候，会依次找这些目录下的html文件，会使用list里先匹配到的那个目录里对应的文件
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'homepage/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**两个方案对比：**

* 共同点：都需要编辑　urls.py　文件；
* 修改settings方案：
    * 方便管理和集成，直接复制粘贴应用的目录，引入和非引入只需要注释和取消注释即可；
    * 但需要注意文件名冲突（即两个应用有模板的文件名相同）；
* 推荐方案：
    * 需要将 templates 文件拷贝到 templates 文件夹中；


**修改settings方案的优化：**

* 以上配置基础上，应用的模板文件名，添加应用名前缀，例如 homepage 应用的 index.html 修改文件名为 homepage_index.html； 

## 5、静态目录

### 5.1、【方案一】简单，但不推荐，适合开发环境使用

简单来说，文件都丢进来，不需要配置路由，只要路径正确，会去找这些文件。

**步骤：**

1. 根目录下新建 ``static``文件夹；
2. settings.py 进行配置，如下：
3. static目录下新建 ``abc.html`` ，body标签内写 ``abc``；
4. 访问　``/abc.html``，会返回 static/abc.html 的内容；

settings.py的配置：

```python
# 这个是配置访问静态文件的路径的，例如 static 下有 abc.html，那么访问路径是 /static/abc.html
STATIC_URL = '/'

# 这个是配置静态文件夹在哪里
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
```

**注意：**

* 默认情况下，静态文件的优先级比路由匹配高；
* 所以建议静态文件的路径应以 static 开头；
* 但是，<b>这样效率极低，也不安全，因此不推荐在生产环境这么做（官方文档如此说的）</b>；

### 5.2【方案二】复杂，但专业，适合生产环境

简单来说，Django 负责路由，而例如 Nginx/CDN 服务器负责处理文件。

参考：https://docs.djangoproject.com/en/2.2/howto/static-files/deployment/

**生产环境：**

settings.py 文件里，DEBUG = False 为生产环境，DEBUG = True 时为开发环境。

**思路：**

1. 将应用（APP）通过配置添加到 settings.py 里；
2. 配置 collectstatic 命令执行后，将静态文件放在哪里；
3. 执行 python manage.py collectstatic 命令，将各个应用（APP）（第一步配置）里的静态文件，放到指定文件夹中去（第二步配置）；
4. 让例如 nginx 服务器指向这个文件夹，想访问指定文件时，就通过 nginx 返回该文件（而不是通过 django 来实现）；

**具体步骤：**

1、将应用添加到配置中。例如有一个 homepage 应用，就如下面这么写:

```python
# 这里添加你配置的 app 名，例如 homepage
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 以上都是默认，下面是新加入的
    'homepage'
]
```

2、配置 collectstatic 命令相关内容，具体见注释：

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 在这里，当访问静态文件时，会自动添加 static
# 例如访问默认应用 admin 时，他会加载 admin/css/base.css，这里配置后，加载的资源链接变为 /static/admin/css/base.css
# 也可以写为：STATIC_URL = 'http://192.168.0.0/static/' 这样的形式（方便CDN）
STATIC_URL = '/static/'

# 配置默认静态文件夹路径
# 在开发环境下，访问静态资源，可以直接访问这里配置的路径下的文件，例如web访问url为 /static/a.html，实际上访问的是根目录下 /static/a.html 这个文件
# 在生产环境下，会将这些目录下的文件复制到 STATIC_ROOT 这里配置的目录中（注意，如果有同名文件，可能会被覆写，他会提示你）
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 目录，是用来将所有 STATICFILES_DIRS 中所有文件夹中的文件，以及各app中（在INSTALLED_APPS里配置）的static中的文件，都复制到这里配置的文件夹中
# 集中之后，方便通过例如 nginx 服务器，或者 CDN 之类的进行部署
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# 这个是默认设置，Django 默认会在 STATICFILES_DIRS 中的文件夹 和 各app下的static文件夹中找文件
# 注意有先后顺序，找到了就不再继续找了
STATICFILES_FINDERS = (
    # 这个先写的话，如果有重复文件，会优先采用 STATICFILES_DIRS 文件夹中的文件
    "django.contrib.staticfiles.finders.FileSystemFinder",
    # 同上，会优先采用应用中的文件
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

```

3、执行 python manage.py collectstatic 命令，他会将 homepage 应用中，static目录下的所有文件，和应用里的文件都复制到 STATIC_ROOT 配置的目录中。

建议先删除该文件夹，再执行命令，否则 overwrite 时，可能会出错。

4、将该静态文件夹丢到nginx或者CDN上去即可。


## 6、返回嵌入数据的模板网页

### 6.1、新建一个应用

```
python manage.py startapp inject_str
```

执行后，文件夹创建完毕。

### 6.2、添加路由（urls.py）

打开 urls.py 文件，做两件事：

1、引入views：

```
from inject_str import views as str_views
```

2、配置路由，在 urlpatterns 这个 list 里添加如下元素

```
path('list/', str_views.index),
```

此时，可以通过路由来访问这个views了，但 views 里的函数还没写好

### 6.3、写渲染函数（views.py）

编辑 inject_str.py 文件，内容如下：

```
from django.shortcuts import render


# Create your views here.
def index(request):
	return render(request, 'inject_str.html', {
		'title': '这里是标题',
		'content': '这里是h1栏',
		'list': [
			'第一行',
			'第二行'
		]
	})
```

此时，渲染函数也写好了，但我们还差一个模板文件。模板文件默认是读取 templates 这个目录里的文件的。


### 6.4、新建一个带模板字符串的html文件

在templates新建一个 inject_str.html 文件，内容如下：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
<h1>{{ content }}</h1>
<ol>
    <li>下面是循环的演示</li>
    {% for i in list %}
        <li>{{ i }}</li>
    {% endfor %}
</ol>
</body>
</html>
```

里面包含：

* 变量名为 title 的字符串，放在 title 标签中；
* 变量名为 content 的字符串，放在 h1 标签中；
* 变量名为 list 的 list，循环产生 li 标签，每个 li 标签的内容是 list 里的一个元素；

即对应 6.3 中 render 函数的第三个参数。

### 6.5、验证

确保你已启动了服务器，不知道如何启动的话，往上翻看第三节。

然后访问 127.0.0.1:8000/list/

显示内容为（html内容）：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>这里是标题</title>
</head>
<body>
<h1>这里是h1栏</h1>
<ol>
    <li>下面是循环的演示</li>
    
        <li>第一行</li>
    
        <li>第二行</li>
    
</ol>
</body>
</html>
```

之所以中间有空行，是因为 for in 函数的原因，这个不影响实际显示，不需要处理。


## 7、异步请求（ajax）的处理

### 7.1、新建一个应用

应用名为：getform

```
python manage.py startapp getform
```

### 7.2、先编辑路由

编辑 urls.py，先引入：

```
from getform import views as form_views
```

然后再配置路由（添加到 urlpatterns）中：

```
# 这个是html
path('form/', form_views.index),
# 这个是处理post提交
path('form/submit', form_views.submit),
```

### 7.3、编辑渲染函数

编辑 getform/viesw.py，内容为：

```
from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
	return render(request, 'form.html')


def submit(request):
	# 判断是 post 请求，注意，这里应是大写
	if request.method == 'POST':
		# 暂时留空
		pass
	return HttpResponse('开发中')
```


### 7.4、添加form表单页面

在 templates 文件夹里添加 form.html，内容如下：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>表单</title>
</head>
<body>
<form action="/form/submit" method="post">
    <p>
        姓名：<input type="text" name="user">
    </p>
    <p>
        年龄：<input type="text" name="age">
    </p>
    <p>
        <input type="submit" value="提交">
    </p>
</form>
</body>
</html>
```

此时查看页面：``http://localhost:8000/form/``，正常。

直接点击提交，进入报错页面，提示内容如下：

```
Forbidden (403)
CSRF verification failed. Request aborted.
```

所谓 CSRF，参考：https://www.cnblogs.com/hyddd/archive/2009/04/09/1432744.html

### 7.5、CSRF处理

在form 标签内加入 ``{% csrf_token %}``，如下：（注意，一定要加到form标签内）

```
<form action="/form/submit" method="post">
    {% csrf_token %}
    <p>
        姓名：<input type="text" name="user">
    </p>
    <p>
        年龄：<input type="text" name="age">
    </p>
    <p>
        <input type="submit" value="提交">
    </p>
</form>
```

效果是form标签内插入了如下标签（示例，value值是随机的）：

```
<input type="hidden" name="csrfmiddlewaretoken" value="BmyyOjDZrFZWBR5gKjKq3d8GCZpeIhn3CPSo5sm4HRaG8UQ2Vx9oq0mnrVAlU7ab">
```

此时再次点击提交按钮，会返回``开发中``三个字符串。

### 7.6、重写处理post请求的函数

重写结果如下：

```
def submit(request):
	print(request.method)
	# 判断是 post 请求，注意要是大写
	if request.method == 'POST':
		# 拿取数据，如果请求方式是 GET 的话，下面应该写为：request.GET.get('user')
		username = request.POST.get('user')
		age = request.POST.get('age')
		# 这个是为了测试没有取到数据的值，测试结果：值为 None
		test = request.POST.get('test')
		print(username, age, test)
		# 返回给用户
		return HttpResponse('你输入的用户姓名是：%s, 年龄是：%s, test 是%s' % (username, age, test))
	else:
		return HttpResponse('没有拿取到数据噢')
```

重新提交，姓名为1，年龄为2，最后跳转到 ``http://localhost:8000/form/submit`` ，显示内容为：

```
你输入的用户姓名是：1, 年龄是：2, test 是None
```

### 7.7、接受JSON格式的请求

以上情况是 form 表单的处理方式。我们常见的请求以JSON形式比较多，那么需要换个方式来处理。

核心步骤如下：

1. 使用 jquery 来发送 json 格式的异步请求；
2. 由于是发送请求，因此要带上csrf（具体处理见以下代码）；
3. django 需要在 body 里拿数据（和form表单不同）；
4. 要调用 json 模块解析 json字符串；
5. 返回信息要包装成 json 字符串，并改写返回信息的header；


#### 7.7.1、使用jquery（示例，也可以用其他的）

重写 templates/form.html 文件，如下：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>表单</title>
    <script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
</head>
<body>
<form action="/form/submit" method="get">
    {% csrf_token %}
    <p>
        姓名：<input type="text" name="user">
    </p>
    <p>
        年龄：<input type="text" name="age">
    </p>
    <p>
        <input type="submit" value="提交">
    </p>
</form>

<button id="submit">点击以JSON格式提交固定内容</button>
<h3>返回信息：<span id="res">空</span></h3>
<script>
    $("#submit").click(function () {
        let data = {
            content: '这里是测试内容'
        }
        $.ajax({
            url: '/form/json',
            type: 'post',
            headers: {
                // 要加 csrf 的请求头，如下
                "X-CSRFToken": '{{ csrf_token }}',
                // 要改请求头，以 json 格式发送信息
                'Content-Type': 'application/json',
            },
            // 发送的数据要先转为 json 格式
            data: JSON.stringify(data),
            // 告诉服务器返回信息要以json格式返回
            dataType: "json",
        }).done(function (result) {
            // 打印返回结果
            console.log(result)
            // 将返回信息插入到页面中
            $("#res").text(result.res)
        })
    })
</script>
</body>
</html>
```

做了几件事：

* 引入jquery；
* 绑定一个click事件；
* headers 添加 csrf 和 ContentType；
* 数据转为 json 字符串；
* 拿取返回信息（默认已经被解析为对象了），显示并插入页面；


#### 7.7.2、添加路由配置

编辑 urls.py ，插入一条路由：

```
# 处理json提交
path('form/json', form_views.postjson),
```

#### 7.7.3、编辑路由处理逻辑

编辑 getform/views.py 文件，插入一个新函数：

```
def postjson(request):
	# time.sleep(10)
	if request.method == 'POST':
		# 拿取数据：json发送post时，数据是在body里
		# 要转为 utf8 格式编码
		# print('request.body: ', request.body)
		data = json.loads(request.body)
		# 此时 data 是一个 dict
		# print('data: ', data)
		res = '你提交的内容是【%s】' % data['content']
		# print('res: ', res)
		result = {
			'res': res
		}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		return HttpResponse('请求类型错误')
```

逻辑参照注释说明。

#### 7.7.4、验证

刷新页面，打开浏览器控制台，点击新增的按钮，查看ajax的发送信息和返回信息。

一切如预期运行。


## 8、django和数据库交互

### 8.0、前注

觉得文章写的对你有帮助，请点赞、关注、Star。

项目资源的github地址：

https://github.com/qq20004604/Python3_Django_Demo

### 8.1、环境安装

首先，确保你安装了mysql。

如果没有安装，就只能和sqlite交互了。

**安装方法：**

可以使用我这里提供的 docker 版 mysql，如果是linux或者MacOS系统，直接运行 sh 文件就能安装了。

https://github.com/qq20004604/docker-learning/tree/master/docker-demo-02-MySQL

可以用安装一个虚拟机，装上centos，然后将文件下载到虚拟机上，运行 create-image-mysql.sh 文件。

装虚拟机的教程参照我这篇文章：

https://blog.csdn.net/qq20004604/article/details/85080666

配置MySQL：（账号密码来自于docker版的配置）

* 账号为 root；
* 密码为 fwefwefvvdsbwrgbr9jj24intwev0h0nbor32fwfmv1；
* 端口（port）为3306；
* IP地址为：xxx；

### 8.2、diango和数据库的交互方式

diango和mysql交互有两种方式：

1. 使用自带的驱动（默认是sqlite3，但可以改为mysql），以ORM形式和mysql交互；
2. 使用第三方的 mysql-connector 数据库，参照廖雪峰的教程：https://www.liaoxuefeng.com/wiki/1016959663602400/1017802264972000 ；或者使用我自己二次封装的：https://github.com/qq20004604/python3-lib/tree/master/mysql_lingling

本文包含： 

* sqlite3；
* ORM形式和mysql交互；
* 多数据库情况下和mysql交互；

通过第三方python和mysql交互的使用方法，可以参考上面2个教程。

方便程度来说，sqlite最方便，第三方也很方便，使用自带mysql驱动最麻烦（版本不对的话要修改配置文件，很坑）。

### 8.3、和sqlite3交互

#### 8.3.1、新建应用：

```
python manage.py startapp withdb
```

然后注册应用，编辑 ``settings.py``，在 INSTALLED_APPS 添加新增应用withdb（homepage是之前添加的）

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 以上都是默认，下面是新加入的
    'homepage',
    'withdb'
]
```

#### 8.3.2、配置model

编辑 ``withdb/models.py`` 文件：

```
from django.db import models


# Create your models here.

# 这个其实就是在建立表结构，使用的是 ORM 的思想
class UserInfo(models.Model):
    # 字段名id，primary_key=True表示主键自增
    id = models.AutoField(primary_key=True)
    # 字段名为username和password，max_length 指这2个字段的最大长度。
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    # 其他参数可选配置包括：（可以点进CharFiled函数查看）
    # verbose_name = None, name = None, primary_key = False,
    # max_length = None, unique = False, blank = False, null = False,
    # db_index = False, rel = None, default = NOT_PROVIDED, editable = True,
    # serialize = True, unique_for_date = None, unique_for_month = None,
    # unique_for_year = None, choices = None, help_text = '', db_column = None,
    # db_tablespace = None, auto_created = False, validators = (),
    # error_messages = None
```

以上作用是设置3个字段：id（自增），username，password

#### 8.3.3、创建 table

执行命令：

```
python manage.py makemigrations
```

这个命令的效果，相当于在该 app（应用）下建立 migrations 目录，并记录下你所有的关于 ``modes.py`` 的改动，比如 ``0001_initial.py``， 但是这个改动还没有作用到数据库文件。

再执行命令：

```
python manage.py migrate
```

这个命令的效果，是将上面的改动，作用到数据库之中。

#### 8.3.4、添加路由

老规矩，修改 ``urls.py`` ，添加路由：

```
# 显示页面
path('user/', db_views.index),
# 注册用户
path('user/register', db_views.register),
# 查看用户列表
path('user/getusers', db_views.getusers)
```

#### 8.3.5、添加异步请求的处理逻辑

修改 ``withdb/views.py``，内容如下：

```
from django.shortcuts import render, HttpResponse
# 引入
from withdb import models
import hashlib
import json


# 返回字符串的 md5 编码
def get_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    # 返回 md5 字符串
    return md5.hexdigest()


# Create your views here.
# 这个是显示页面的逻辑（好吧，也没啥逻辑可说）
def index(request):
    return render(request, 'users.html')


# 这个是注册的逻辑
def register(request):
    print('register')
    if not request.method == 'POST':
        return HttpResponse(json.dumps({'code': 0, 'msg': '请求类型错误'}), content_type="application/json")

    # 如果是 POST 请求
    data = json.loads(request.body)
    username = data["username"]
    pw = data["pw"]
    err = None
    # 先验证一下是否符合要求
    if len(username) > 20 or len(pw) > 20:
        err = '用户名或者密码长度过长'
    if len(username) < 8 or len(pw) < 8:
        err = '用户名或密码长度过短（不应短于8位）'

    # 如果有报错信息，则返回
    if not err == None:
        return HttpResponse(json.dumps({'code': 0, 'msg': err}), content_type="application/json")

    # 截取md5前20位（避免明文密码存取）
    md5_pw = get_md5(pw)[0:20]
    # 一切顺利保存到数据库
    save_success = True
    # 防止存储失败
    msg = 'success'
    try:
        # 这个的返回值，是当前 list 的所有值
        models.UserInfo.objects.create(username=username, password=md5_pw)
    except BaseException as e:
        save_success = False
        with open('./log.log', 'a') as f:
            f.write('username = %s ,pw = %s , error = %s\n' % (username, pw, e))
    print(save_success, msg, '-------------------')
    if save_success:
        return HttpResponse(json.dumps({'code': 0, 'msg': msg}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'code': 0, 'msg': '发生未知错误'}), content_type="application/json")


# 这个是获取用户列表的逻辑
def getusers(request):
    user_list = models.UserInfo.objects.all()
    list = []
    # user_list　是一个 <class 'django.db.models.query.QuerySet'>
    for i in user_list:
        # i 是一个 <class 'withdb.models.UserInfo'> ，注意，不要把pw返回回去了
        list.append({
            'username': i.username,
            'id': i.id
        })
    result = {'code': 0, 'data': list}
    return HttpResponse(json.dumps(result), content_type="application/json")
```

分为三部分：

1. 返回页面；
2. 注册用户；
3. 显示用户列表；

第二步中，注册用户应该先查询，然后排除重复的用户名，不重复才能注册，这里省略掉了（因为第三步已经有相关逻辑，这里只是教程所以没写出来）

#### 8.3.6、写前端页面

templates 目录下创建 user.html

内容如下：

```
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>用户</title>
    <script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
</head>
<body>
<p>
    用户列表
    <button id="getlist">点击刷新</button>
</p>
<ul id="list">
    <li>空</li>
</ul>

<div>
    <h2>注册</h2>
    <p>用户名：<input type="text" id="username"></p>
    <p>密码：<input type="text" id="pw"></p>
    <p>
        <button id="register">注册</button>
    </p>
    <p id="msg"></p>
</div>
<script>
    let csrf_token = '{{ csrf_token }}'
    $(function () {
        $("#getlist").click(function () {
            $.ajax({
                url: '/user/getusers',
                type: 'get',
                headers: {
                    // 要加 csrf 的请求头，如下
                    "X-CSRFToken": csrf_token
                },
                // 告诉服务器返回信息要以json格式返回
                dataType: "json",
            }).done(function (result) {
                // 打印返回结果
                console.log(result)
                // 将返回信息插入到页面中
                let text = result.data.map(user => {
                    return `<li>用户id：${user.id}，用户名：${user.username}</li>`
                }).join('')
                if (text.length === 0) {
                    text = '<li>没有加载到数据</li>'
                }
                $("#list").html(text)
            })
        })

        $("#register").click(function () {
            $.ajax({
                url: '/user/register',
                type: 'post',
                headers: {
                    // 要加 csrf 的请求头，如下
                    "X-CSRFToken": csrf_token,
                    // 要改请求头，以 json 格式发送信息
                    'Content-Type': 'application/json',
                },
                // 发送的数据要先转为 json 格式
                data: JSON.stringify({
                    username: $("#username").val(),
                    pw: $("#pw").val()
                }),
                // 告诉服务器返回信息要以json格式返回
                dataType: "json",
            }).done(function (result) {
                // 打印返回结果
                console.log(result)
                // 将返回信息插入到页面中
                $("#msg").html(result.msg)
            })
        })
    })
</script>
</body>
</html>
```

两个功能：

* 显示用户列表；
* 注册新用户；

#### 8.3.7、梳理逻辑和验证

1、用户访问链接 /user/ 显示页面（templates/user.html）；

2、页面里有两个功能：【显示用户列表】和【注册新用户】

3、显示用户列表：将请求链接：``/user/getusers``，然后通过 ORM 表结构（``widthdb/models.py``）来读取数据库，并通过 ``widthdb/views.py`` 的 getusers 函数返回相关信息；

4、注册用户：以异步请求的方式将username和password字段通过 ``/user/getusers`` 传入到 ``widthdb/views.py`` 的 register 函数来处理。在注册前，会验证一下数据是否符合要求。不符合则提示错误信息，符合则将数据插入到数据库之中；

分别点击页面的 点击刷新按钮，和注册按钮，发现可以正常运行（可以参考我的代码 https://github.com/qq20004604/Python3_Django_Demo ）

### 8.4、和mysql交互（ORM形式）

#### 8.4.1、简述

方式和8.3的 sqlite3 使用方式几乎一样，唯一区别是存到 mysql 里，而不是 sqlite 里。

这里使用的是django默认和mysql交互的方式来实现的。（不需要手写sql，通过ORM形式实现和数据库的管理）

#### 8.4.2、引入mysql驱动

1、python和mysql交互，需要装一个驱动：

```
pip install pymysql
```

2、然后编辑 ``urls.py`` 同级目录的 ``__init__.py``，添加内容：

```
import pymysql

pymysql.install_as_MySQLdb()
```

3、但是报错：

```
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.
```

查找N篇解决方案，此方案可供参考：

https://blog.csdn.net/weixin_33127753/article/details/89100552

选用方案二：【删除源代码的警告代码！】（真TM暴力）

简单来说，就是注释掉那行报错的判断信息就行了。

4、注释后，有红字提示：

```
You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

意思是你的应用数据库没迁移（指没从sqlite3迁移到mysql里）。


#### 8.4.3、配置database

编辑 ``settings.py`` 的 DATABASES 属性，如下：

```
DATABASES = {
	# 这里是和mysql交互
	'default': {
		'ENGINE': 'django.db.backends.mysql',  # 数据库引擎，这个用的是pymysql，具体见官方文档
		'NAME': 'django',  # 这里是database 名
		'USER': 'root',  # 为了方便，用root，实际应用中应添加特定用户
		'PASSWORD': 'fwefwefvvdsbwrgbr9jj24intwev0h0nbor32fwfmv1',  # 密码
		'HOST': '127.0.0.1',  # mysql服务所在的主机ip，这里是在本机用的docker装的mysql，所以是127.0.0.1
		'PORT': '3306',  # mysql服务端口
		'OPTIONS': {
			'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
		}
	}
}
```

#### 8.4.4、数据库准备

1、在数据库里建立 database（名字等于上面 mysqldb 配置中 NAME 的值）；

```
create database django;
```

2、初始化数据库的表配置：

记录改动：

```
python manage.py makemigrations
```


插入到数据库中：

```
python manage.py migrate
```

3、查看数据库

进入mysql，然后 ``use [database_name];``，再查看有哪些表 ``show tables;``（可以看到有一个表格django_migrations），再查看表内容 ``select * from django_migrations;``，发现是有数据的。

```
mysql> show tables;
+----------------------------+
| Tables_in_django           |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| withdb_userinfo            |
+----------------------------+
11 rows in set (0.01 sec)
```

#### 8.4.5、其他配置

参考8.3.4、8.3.5、8.3.6，这个时候刷新数据。

验证后可以发现和sqlite版一样正常运行。

### 8.5、多数据库配置

这里指：

* 同时使用sqlite3和mysql；
* 或者mysql使用不同database；
* 或者直接就是不同server的mysql数据库；


#### 8.5.1、修改 ``settings.py``

修改 ``settings.py``，先修改 DATABASE的配置：

```
DATABASES = {
    'sqlitedb': {
        # 之前的sqlite3配置
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3.bak'),
    },
    # 这里是和mysql交互，用于配置默认的那些app
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎，这个用的是pymysql，具体见官方文档
        'NAME': 'django_default',  # 这里是database 名
        'USER': 'root',  # 为了方便，用root，实际应用中应添加特定用户
        'PASSWORD': 'fwefwefvvdsbwrgbr9jj24intwev0h0nbor32fwfmv1',  # 密码
        'HOST': '127.0.0.1',  # mysql服务所在的主机ip，这里是在本机用的docker装的mysql，所以是127.0.0.1
        'PORT': '3306',  # mysql服务端口
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
    # 这里是和mysql交互，用于 withdb 这个应用使用
    'userdb': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎，这个用的是pymysql，具体见官方文档
        'NAME': 'django',  # 这里是database 名
        'USER': 'root',  # 为了方便，用root，实际应用中应添加特定用户
        'PASSWORD': 'fwefwefvvdsbwrgbr9jj24intwev0h0nbor32fwfmv1',  # 密码
        'HOST': '127.0.0.1',  # mysql服务所在的主机ip，这里是在本机用的docker装的mysql，所以是127.0.0.1
        'PORT': '3306',  # mysql服务端口
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

再添加两行配置：

```
# 多应用的db路由
DATABASE_ROUTERS = ['Python3_Django_Demo.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    # example:
    # 'app_name':'database_name',
    # 这些是默认应用
    'admin': 'default',
    'auth': 'default',
    'contenttypes': 'default',
    'sessions': 'default',
    'messages': 'default',
    'staticfiles': 'default',
    # 这些是自定义应用
    'withdb': 'userdb',
}
```

以上配置表示，使用 ``database_router.py`` 文件里的 DatabaseAppsRouter 函数来处理路由。

以及不同app默认使用不同的db设置（也可以在实际使用的时候，手动指定具体使用哪一个）

#### 8.5.2、编写db的路由函数

在 ``settings.py`` 同目录下，新建 ``database_router.py`` 文件。

内容如下：

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING


class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}

    这个路由，针对对不同的数据库，用于操作所有的数据库模型

    如果一个应用没有在 settings 里的 DATABASE_APPS_MAPPING 中配置，那么这个路由将最后被 default 这个数据库来配置

    设置示例（这里指 DATABASE_APPS_MAPPING 属性）：

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """

    def db_for_read(self, model, **hints):
        """"
        Point all read operations to the specific database.
        将所有读取操作，指向对特定的数据库
        """
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Point all write operations to the specific database.
        将所有的写操作，指向特定的数据库
        """
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between apps that use the same database.
        允许 任何使用相同数据库的应用 的任何关系
        """
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    # Django 1.7 - Django 1.11
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print
        db, app_label, model_name, hints
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(app_label) == db
        elif app_label in DATABASE_MAPPING:
            return False
        return None
```

#### 8.5.3、数据库准备

我们依然需要进行数据库准备。

首先需要创建2个database，分别是：``django_default`` 和 ``django`` 这2个。

然后执行以下三行代码做数据库的准备（创建table等）

记录改动：

```
python manage.py makemigrations
```

插入到数据库中：(后面的名字是下面DATABASES的属性的key值）

```
python manage.py migrate
python manage.py migrate --database=userdb
```

上面两行 migrate ，不带参数的，只生成default里配置的那些app的table。

带参数的，生成 DATABASES 这个 dict 里 key 为 userdb ，跟他相关的应用所需要的 table。

#### 8.5.4、其他

其他的复用之前使用默认mysql配置的代码，不需要改动。

唯一需要提一下的是，在 ``views.py`` 里操作数据库，我们之前使用代码例如：

```
models.UserInfo.objects.all()
```

这里是使用默认指定的db，我们也可以使用指定db，如下：

```
models.UserInfo.objects.using('userdb').all()
```

源代码参照我的github项目：（安装好依赖后就直接能跑）

https://github.com/qq20004604/Python3_Django_Demo
