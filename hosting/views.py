from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from hosting import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import XML

try:
    from django.utils import simplejson as json
except ImportError:
    import json
import re

def generateSampleDir():
    return {
        'path': ['dir1', 'dir2', 'dir3'],
        'content': {
            'dir1' : {'type': 'd', 'size': 0, 'date': '12-04-2018', 'owner': 'Martin'},
            'file1': {'type': 'f', 'size': 5, 'date': '12-01-2018', 'owner': 'Martin'},
            'file2': {'type': 'f', 'size': 10, 'date': '12-02-2018', 'owner': 'Jan'},
            'file3': {'type': 'f', 'size': 15, 'date': '12-03-2018', 'owner': 'Ondrej'}
        }
    }

def generateHierarchy(l):
    #print(l)
    return {
        'path': l,
        'content': {
            'file1': {'type': 'f', 'size': 1, 'data': '1-1-1970', 'owner': 'Martin'},
            'dir': {'type': 'd'}
        }
    }


def index(request):
    #User.objects.all().delete()
    #u = User(name="Martin", surname="Beneš", email="martinbenes1996@gmail.com")
    #u.save()
    if request.method == 'POST':
        pk = request.POST.get('pk')
        User.objects.get(pk=pk).delete()
        return HttpResponseRedirect('')
    authors = User.objects.all()
    return render(request, "homepage.html", {"authors": authors})

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


        user = User.objects.create_user(d['email'], password='')
        user.email = d['email']
        user.first_name = d['name']
        user.last_name = d['surname']
        user.save()
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
            user = authenticate(username=d['email'], password='')
            if user is not None:
                response = redirect('dashboard')
                response.set_cookie('user', d['email'], max_age=7200)
                return response
            else:
                d['message'] = 'No user with given email'

        if 'message' in d:
            return render(request, "login.html", d)
    else:
        return render(request, "login.html", {})

def info(request):
    authors = User.objects.all()
    return render(request, "info.html", {"authors": authors})

def dashboard(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    else:
        d['page_list'] = models.Webpage.getWebpages(d['user'])

    return render(request, "dashboard.html", d)

def pageboard(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    else:
        pass

    return render(request, "pageboard.html", d)

def createpage(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    else:
        if request.method == 'POST':
            d['name'] = request.POST['name']
            w = models.Webpage(name=d['name'], user=d['user'])
            w.save()

    return redirect('dashboard')

def logout(request):
    response = redirect('')
    response.delete_cookie('user')
    return response

@csrf_exempt
def getDirData(request):
    if request.method == 'POST':
        path = json.loads( request.POST['requestpath'] )
        print(path)
        jsonresponse = json.dumps(XML.GetInfoFromFiletree("id101", path))
        #jsonresponse = json.dumps(generateHierarchy(path))
        #jsonresponse = json.dumps(generateSampleDir())
        return HttpResponse(jsonresponse, content_type='application/json')



# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information
