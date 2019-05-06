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
