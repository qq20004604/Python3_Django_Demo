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
