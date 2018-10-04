from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
   text = "<h1>Hello, World!</h1>"
   return HttpResponse(text)

def index(request):
   return render(request, "index.html", {})