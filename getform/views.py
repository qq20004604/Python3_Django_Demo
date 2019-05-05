from django.shortcuts import render, HttpResponse
import time
import json


# Create your views here.
def index(request):
	return render(request, 'form.html')


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


def postjson(request):
	# time.sleep(10)
	if request.method == 'POST':
		# 拿取数据：json发送post时，数据是在body里
		# 要转为 utf8 格式编码
		print('request.body: ', request.body)
		data = json.loads(request.body)
		# 此时 data 是一个 dict
		print('data: ', data)
		res = '你提交的内容是【%s】' % data['content']
		print('res: ', res)
		result = {
			'res': res
		}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		return HttpResponse('请求类型错误')
