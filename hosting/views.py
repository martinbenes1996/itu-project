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
    ''' Tady formát sedí '''
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

def generateDatabase():
    '''
        example:
                [{tablename,row_data,definition_of_rows},{...},...]
                    - row_data = [['polozky','dle','definice','radku'],[...],...]
                    - definition_of_rows = [["rowname","rowdatatype"],[...],...]

                [
                 {'name': 'hrusky',
                  'rows': [],
                  'definition': [['id','i'],['jmeno','s'],['odruda','s']]},

                 {'name': 'jabka',
                  'rows': [['0', 'Granny Smith', 'green'], ['1', 'Granny Smith', 'green'],['2', 'Granny Smith', 'green']],
                  'definition': [['id','i'],['jmeno','s'],['barva','s']]}
                ]
    '''
    return {
        'name': 'databaze1',
        'tables': {
            'tabulka1': {
                'columns': {
                    'jmeno': 's',
                    'prijmeni': 's',
                    'stastne_cislo': 'i'
                },
                'data': [
                    {'jmeno': 'matej', 'prijmeni': 'navratil', 'stastne_cislo': 666},
                    {'jmeno': 'adolf', 'prijmeni': 'hitler', 'stastne_cislo': 13},
                    {'jmeno': 'ondrej', 'prijmeni': 'polansky', 'stastne_cislo': 42},
                    {'jmeno': 'martin', 'prijmeni': 'benes', 'stastne_cislo': 69}
                ]
            },
            'tabulka2': {
                'columns': {
                    'carodej': 's',
                    'kouzlo': 's'
                },
                'data': [
                    {'carodej': 'kolovrat', 'kouzlo': 'abrakadabra'},
                    {'carodej': 'uchomaz', 'kouzlo': 'ententyky'},
                    {'carodej': 'lapiduch', 'kouzlo': 'popokatepetl'}
                ]
            }
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
    pageid = request.GET['id']
    d['page'] = models.Webpage.objects.get(id=pageid)

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
            XML.CreateProject(d['name'])
            w = models.Webpage(name=d['name'], user=d['user'])
            w.save()

    return redirect('dashboard')

def logout(request):
    response = redirect('')
    response.delete_cookie('user')
    return response

@csrf_exempt
def getDirData(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        path = json.loads( request.POST['requestpath'] )
        project = request.POST['projname']
        print(project, path)
        jsonresponse = json.dumps(XML.GetInfoFromFiletree(project, path))
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def renameFile(request):
    if request.method == 'POST':
        path = json.loads( request.POST['requestpath'] )
        oldname = request.POST['origname']
        newname = request.POST['newname']
        print(path, ':', oldname, '->', newname)
        #tady nastavit v XML
        return getDirData(request)

@csrf_exempt
def deleteFile(request):
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        name = request.POST['name']
        XML.DeleteFromFiletree(projname, path, name)
        return getDirData(request)

@csrf_exempt
def createDir(request):
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        name = request.POST['name']
        XML.AddToFiletree(projname, path, name, 'd')
        return getDirData(request)

@csrf_exempt
def createFile(request):
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        name = request.POST['name']
        size = request.POST['size']
        XML.AddToFiletree(projname, path, name, 'f', "unknown", size)
        return getDirData(request)


@csrf_exempt
def getDbData(request):
    if request.method == 'POST':
        jsonresponse = json.dumps(generateDatabase())
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def getUserData(request):
    if request.method == 'POST':
        projname = request.POST['projname']
        jsonresponse = json.dumps(XML.GetUser(projname))
        print(jsonresponse)
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        projname = request.POST['projname']
        username = request.POST['username']
        XML.AddUser(projname, username)
        return getUserData(request)

@csrf_exempt
def deleteUser(request):
    if request.method == 'POST':
        projname = request.POST['projname']
        username = request.POST['username']
        XML.DeleteUser(projname, username)
        return getUserData(request)


# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information
