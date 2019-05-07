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
