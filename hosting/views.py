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

def enc(userPk, projName):
    ''' encode project name '''
    return str(userPk)+"_"+str(projName)

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
            # second argument is owner, default=unknown
            try:
                XML.CreateProject( enc(d['user'].pk,d['name']) )
            except:
                # project already exists !!! Send error message !!!
                return redirect('dashboard')
            w = models.Webpage(name=d['name'], user=d['user'])
            w.save()

    return redirect('dashboard')

def logout(request):
    response = redirect('')
    response.delete_cookie('user')
    return response

def deletepage(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    else:
        if request.method == 'POST':
            project = request.POST['projname']
            XML.DeleteProject( enc(d['user'].pk,project) )
            # nejsem si jistý nasledujicima dvema radkama !!!
            w = models.Webpage.objects.get(name=project, user=d['user'].pk)
            w.remove()

    return redirect('dashboard')

def renamepage(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    else:
        if request.method == 'POST':
            oldproject = request.POST['projname']
            newproject = request.POST['newprojname']
            try:
                XML.RenameProject( enc(d['user'].pk,oldproject), enc(d['user'].pk,newproject) )
            except AlreadyExistsError:
                # newproject already exists !!! Send error message !!!
                return redirect('dashboard')
            except AlreadyExistsError:
                # oldproject does not exist !!! Send error message !!!
                return redirect('dashboard')
            # nejsem si jistý nasledujicima dvema radkama !!!
            w = models.Webpage.objects.get(name=oldproject, user=d['user'].pk)
            w.name = str(newproject)
            w.save()

    return redirect('dashboard')

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
        jsonresponse = json.dumps(XML.GetInfoFromFiletree(enc(d['user'].pk,project), path))
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def createDir(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        name = request.POST['name']
        XML.AddToFiletree(enc(d['user'].pk,projname), path, name, 'd')
        return getDirData(request)

@csrf_exempt
def createFile(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        name = request.POST['name']
        size = request.POST['size']
        XML.AddToFiletree(enc(d['user'].pk,projname), path, name, 'f', "unknown", size)
        return getDirData(request)

@csrf_exempt
def renameFile(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        oldname = request.POST['origname']
        newname = request.POST['newname']
        print(path, ':', oldname, '->', newname)
        XML.RenameInFiletree(enc(d['user'].pk,projname), path, oldname, newname)
        return getDirData(request)

@csrf_exempt
def deleteFile(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        path = json.loads( request.POST['requestpath'] )
        name = request.POST['name']
        XML.DeleteFromFiletree(enc(d['user'].pk,projname), path, name)
        return getDirData(request)

# -------------- DATABASE --------------
@csrf_exempt
def getDbData(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        jsonresponse = json.dumps(generateDatabase())
        return HttpResponse(jsonresponse, content_type='application/json')





# dns, user, email funkce maji stejne argumenty a operace, lisi se jen nazvem
@csrf_exempt
def getUserData(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        jsonresponse = json.dumps(XML.GetUser(enc(d['user'].pk,projname)))
        print(jsonresponse)
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def addUser(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        username = request.POST['username']
        XML.AddUser(enc(d['user'].pk,projname), username)
        return getUserData(request)

@csrf_exempt
def deleteUser(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        username = request.POST['username']
        XML.DeleteUser(enc(d['user'].pk,projname), username)
        return getUserData(request)

@csrf_exempt
def renameUser(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        newusername = request.POST['newusername']
        oldusername = request.POST['oldusername']
        XML.DeleteUser(enc(d['user'].pk,projname), oldusername)     # might be changed in the future
        XML.AddUser(enc(d['user'].pk,projname), newusername)
        return getUserData(request)

@csrf_exempt
def getDnsData(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        jsonresponse = json.dumps(XML.GetDNS(enc(d['user'].pk,projname)))
        print(jsonresponse)
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def addDns(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        dnsname = request.POST['dnsname']
        XML.AddDNS(enc(d['user'].pk,projname), dnsname)
        return getDnsData(request)

@csrf_exempt
def deleteDns(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        dnsname = request.POST['dnsname']
        XML.DeleteDNS(enc(d['user'].pk,projname), dnsname)
        return getDnsData(request)

@csrf_exempt
def renameDns(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        newdnsname = request.POST['newdnsname']
        olddnsname = request.POST['olddnsname']
        XML.DeleteDNS(enc(d['user'].pk,projname), olddnsname)     # might be changed in the future
        XML.AddDNS(enc(d['user'].pk,projname), newdnsname)
        return getDnsData(request)

@csrf_exempt
def getEmailData(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        jsonresponse = json.dumps(XML.GetEmail(enc(d['user'].pk,projname)))
        print(jsonresponse)
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def addEmail(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        emailname = request.POST['emailname']
        XML.AddEmail(enc(d['user'].pk,projname), emailname)
        return getEmailData(request)

@csrf_exempt
def deleteEmail(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        emailname = request.POST['emailname']
        XML.DeleteEmail(enc(d['user'].pk,projname), emailname)
        return getEmailData(request)

@csrf_exempt
def renameEmail(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        newemailname = request.POST['newemailname']
        oldemailname = request.POST['oldemailname']
        XML.DeleteEmail(enc(d['user'].pk,projname), oldemailname)     # might be changed in the future
        XML.AddEmail(enc(d['user'].pk,projname), newemailname)
        return getEmailData(request)



# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information
