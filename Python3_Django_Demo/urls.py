"""Python3_Django_Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# 引入项目
from homepage import views as homepage_views
from inject_str import views as str_views
from getform import views as form_views
from withdb import views as db_views
from dynamic_template import views as dy_views

# 这里配置 url
urlpatterns = [
    path('', homepage_views.index),
    path('list/', str_views.index),
    path('admin/', admin.site.urls),
    # 这个是html
    path('form/', form_views.index),
    # 这个是处理post提交
    path('form/submit', form_views.submit),
    # 处理json提交
    path('form/json', form_views.postjson),
    # 显示页面
    path('user/', db_views.index),
    # 注册用户
    path('user/register', db_views.register),
    # 查看用户列表
    path('user/getusers', db_views.getusers),
    # 动态数据嵌入页面
    path('dy/', dy_views.index),
]
