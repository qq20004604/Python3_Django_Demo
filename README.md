# Python3_Django_Demo


## 0、说明

版本：

```
django版本：2.2.1
python版本：3.7
```

配置：

```
默认用户名 wd 默认密码 yjQeZ3PDmhVudTR
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


## 7、获取用户发送的信息

### 7.1、获取 form 表单发送信息

