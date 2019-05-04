from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    # return HttpResponse('Home Page')
    return render(request, 'homepage_default.html')
