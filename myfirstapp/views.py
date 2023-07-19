from django.shortcuts import render
from django.http import HttpResponse


## This return a simple http response
#def say_hello(request):
#    return HttpResponse('Hello World')
#

# This return a rendered html to the client using `render`
def say_hello(request):
    x = 1
    y = 2
    return render(request, 'hello.html', context={'name': 'juliano'})
