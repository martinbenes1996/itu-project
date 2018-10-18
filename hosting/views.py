from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from hosting.models import User
from django.core.exceptions import ObjectDoesNotExist
import re

def index(request):
    #User.objects.all().delete()
    #u = User(name="Martin", surname="Beneš", email="martinbenes1996@gmail.com")
    #u.save()
    if request.method == 'POST':
        pk = request.POST.get('pk')
        User.objects.get(pk=pk).delete()
        return HttpResponseRedirect('')
    authors = User.objects.all()
    return render(request, "index.html", {"authors": authors})

def register(request):
    if request.method == 'POST':
        d = {'name':'', 'surname':'', 'email':''}
        try:
            d['name'] = request.POST['name']
        except KeyError:
            d['message'] = 'No name given'

        d['surname'] = request.POST.get('surname', '')
        try:
            d['email'] = request.POST['email']
        except KeyError:
            d['message'] = 'No email given'
        if re.match(r'.+@.+\..+', d['email']) == None:
            d['message'] = 'Invalid email'
        try:
            u = User.objects.get(email=d['email'])
        except:
            pass
        else:
            d['message'] = 'Given email already used'

        if 'message' in d:
            return render(request, "register.html", d)
        
        u = User(name=d['name'], surname=d['surname'], email=d['email'])
        u.save()
        return redirect('')
    else:
        return render(request, "register.html", {})

def login(request):
    if request.method == 'POST':
        d = {'email':''}
        try:
            d['email'] = request.POST['email']
        except KeyError:
            d['message'] = 'No email given'
        else:
            try:
                u = User.objects.get(email=d['email'])
            except ObjectDoesNotExist:
                d['message'] = 'No user with given email'

        if 'message' in d:
            return render(request, "login.html", d)

        return redirect('')
    else:
        return render(request, "login.html", {})


# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information