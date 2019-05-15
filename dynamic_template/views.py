from django.shortcuts import render

from key_value_controller import c

# 注册key
c.register_key('foo', 'default foo', expire_time=5000)


# 查看当前值（即默认值），这里应该是 default foo
# print(c.get_value('foo'))


# Create your views here.
def index(request):
    # return HttpResponse('Home Page')
    return render(request, 'dynamic.html', {
        'foo': c.get_value('foo')
    })
