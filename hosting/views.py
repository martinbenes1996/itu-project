from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from hosting import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import XML
#import xml.etree.ElementTree as ET
from lxml import etree as ET

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
    '''
    return [
                 {'name': 'hrusky',
                  'rows': [],
                  'definition': [['id','i'],['jmeno','s'],['odruda','s']]},

                 {'name': 'jabka',
                  'rows': [['0', 'Granny Smith', 'green'], ['1', 'Moje jabko', 'red'],['2', 'Taiwanska namka', 'orange']],
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
    '''


def index(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
        d['logged'] = True
    except ObjectDoesNotExist:
        d['logged'] = False
    if request.method == 'POST':
        pk = request.POST.get('pk')
        User.objects.get(pk=pk).delete()
        return HttpResponseRedirect('')
    d['authors'] = User.objects.all()
    return render(request, "homepage.html", d)

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
                d['message'] = 'Project already exists.'
                return redirect('dashboard')
            w = models.Webpage(name=d['name'], user=d['user'])
            w.save()

    return redirect('dashboard')

def logout(request):
    response = redirect('')
    response.delete_cookie('user')
    return response

@csrf_exempt
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
            try:
                XML.DeleteProject( enc(d['user'].pk,project) )
            except:
                pass
            try:
                models.Webpage.objects.get(name=project, user=d['user']).delete()
            except:
                pass

    return redirect('dashboard')

@csrf_exempt
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
            except XML.AlreadyExistsError:
                d['message'] = 'New project already exists.'
                return redirect('dashboard')
            except XML.AlreadyExistsError:
                d['message'] = 'Old project does not exist.'
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
        try:
            jsonresponse = json.dumps(XML.GetInfoFromFiletree(enc(d['user'].pk,project), path))
        except XML.DoesNotExistError:
            d['message'] = 'Directory with given path does not exist.'
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
        try:
            XML.AddToFiletree(enc(d['user'].pk,projname), path, name, 'd')
        except XML.NameContainsWrongCharError:
            d['message'] = 'File/dir name contains unacceptable characters (only [a-zA-Z0-9_.]).'
        except XML.DoesNotExistError:
            d['message'] = 'Path or directory does not exist.'
        except XML.WrongTypeError:
            d['message'] = 'You cannot put things into file.'
        except XML.AlreadyExistsError:
            d['message'] = 'File/dir with the same name already exists.'
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
        try:
            XML.AddToFiletree(enc(d['user'].pk,projname), path, name, 'f', "unknown", size)
        except XML.NameContainsWrongCharError:
            d['message'] = 'File/dir name contains unacceptable characters (only [a-zA-Z0-9_.]).'
        except XML.DoesNotExistError:
            d['message'] = 'Path or directory does not exist.'
        except XML.WrongTypeError:
            d['message'] = 'You cannot put things into file.'
        except XML.AlreadyExistsError:
            d['message'] = 'File/dir with the same name already exists.'
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
        try:
            XML.RenameInFiletree(enc(d['user'].pk,projname), path, oldname, newname)
        except XML.NameContainsWrongCharError:
            d['message'] = 'File/dir name contains unacceptable characters (only [a-zA-Z0-9_.]).'
        except XML.DoesNotExistError:
            d['message'] = 'File/dir does not exist.'
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
        try:
            XML.DeleteFromFiletree(enc(d['user'].pk,projname), path, name)
        except XML.DoesNotExistError:
            d['message'] = 'File/dir does not exist.'
        return getDirData(request)

# -------------- DATABASE --------------
@csrf_exempt
def getTableNames(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        try:
            #print( XML.GetTableNames(enc(d['user'].pk,projname)) )
            jsonresponse = json.dumps(XML.GetTableNames(enc(d['user'].pk,projname)))
        except:
            d['message'] = 'XML error, users do not exist.'
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def getDbData(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        #p = XML.GetTableContent( "dat007", "jabka" )   # get table as a xml string
        p = XML.GetTableContent(enc(d['user'].pk,projname),tablename)
        #print(p)

        xml = ET.fromstring(p)                              # load raw xml
        xsl = ET.parse("trnsfrm.xsl")                       # load raw xsl
        transform = ET.XSLT(xsl)                            # create transform formula from xsl
        result = transform(xml)                             # transform xml

        jsonresponse = json.dumps({'html': str(result)})                          # send via json as string
        return HttpResponse(jsonresponse, content_type='application/json')

@csrf_exempt
def createTable(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        # definition is a list of lists like this: [["nazev sloupce","datovy typ"],...]
        # je treba to tu nejak poskladat, musi to byt seznamy kvuli poradi zaznamu...
        #definition = [["id","i"],["name","s"]]      # temporary definition
        definition = json.loads( request.POST['definition'] )

        # odstran
        #print(tablename, definition)
        #print(getTableNames(request))
        #return getTableNames(request)
        # odstran

        try:
            XML.CreateTable(enc(d['user'].pk,projname), tablename, definition)
        except XML.DoesNotExistError:
            d['message'] = 'Database does not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'Table already exists.'
        return getTableNames(request)

@csrf_exempt
def modifyTable(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        newtablename = json.loads( request.POST['newtablename'] )
        try:
            XML.ModifyTable(enc(d['user'].pk,projname), tablename, newtablename)
        except XML.DoesNotExistError:
            d['message'] = 'Database does not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'Table already exists.'
        return getTableNames(request)

@csrf_exempt
def deleteTable(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']

        try:
            XML.DeleteTable(enc(d['user'].pk,projname), tablename)
        except XML.DoesNotExistError:
            d['message'] = 'Database or table does not exist.'
        return getTableNames(request)

@csrf_exempt
def editRow(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        # rowdata is a list of data: ["prvni sloupec","druhy sloupec",...]
        # je treba to tu nejak poskladat, musi to byt seznam kvuli poradi zaznamu...
        #rowdata = ["0","pepa"]      # temporary data
        rowdata = json.loads( request.POST['rowdata'] )

        try:
            XML.AddRow(enc(d['user'].pk,projname), tablename, rowdata)
        except XML.DoesNotExistError:
            d['message'] = 'Database or table does not exist.'
        except XML.IncompatibleRowDataError:
            d['message'] = 'Row data incompatible.'
        except XML.TableNotFoundError:
            d['message'] = 'Table was not found.'
        #print(d['message'])
        return getDbData(request)

@csrf_exempt
def addRow(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        # rowdata is a list of data: ["prvni sloupec","druhy sloupec",...]
        # je treba to tu nejak poskladat, musi to byt seznam kvuli poradi zaznamu...
        #rowdata = ["0","pepa"]      # temporary data
        rowdata = json.loads( request.POST['rowdata'] )

        rowdata[0] = XML.GenerateID(enc(d['user'].pk,projname), tablename)

        try:
            XML.AddRow(enc(d['user'].pk,projname), tablename, rowdata)
        except XML.DoesNotExistError:
            d['message'] = 'Database or table does not exist.'
        except XML.IncompatibleRowDataError:
            d['message'] = 'Row data incompatible.'
        except XML.TableNotFoundError:
            d['message'] = 'Table was not found.'
        #print(d['message'])
        return getDbData(request)


@csrf_exempt
def deleteRow(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        rowid = request.POST['rowid']

        # id of the row (hodnota primarniho klice, vzdy je v prvnim sloupci, muze to byt cokoli - cislo/string)
        try:
            XML.DeleteRow(enc(d['user'].pk,projname), tablename, rowid)
        except XML.DoesNotExistError:
            d['message'] = 'Database or table does not exist.'
        return getDbData(request)

@csrf_exempt
def addColumn(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        column = request.POST['column']
        # priklad: ["name","s"] - nazev sloupce + datovy typ
        defaultvalue = request.POST['defaultvalue']
        try:
            XML.AddColumn(enc(d['user'].pk,projname), tablename, column, defaultvalue)
        except XML.DoesNotExistError:
            d['message'] = 'Database does not exist.'
        return getDbData(request)

@csrf_exempt
def modifyColumn(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        column = request.POST['column']
        newcolumnname = request.POST['newcolumnname']
        try:
            XML.ModifyColumn(enc(d['user'].pk,projname), tablename, column, newcolumnname)
        except XML.DoesNotExistError:
            d['message'] = 'Database does not exist.'
        return getDbData(request)

@csrf_exempt
def deleteColumn(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        d['user'] = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    if request.method == 'POST':
        projname = request.POST['projname']
        tablename = request.POST['tablename']
        columnname = request.POST['columnname']     # name of the deleted column
        try:
            XML.DeleteColumn(enc(d['user'].pk,projname), tablename, columnname)
        except XML.DoesNotExistError:
            d['message'] = 'Database does not exist.'
        return getDbData(request)

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
        try:
            jsonresponse = json.dumps(XML.GetUser(enc(d['user'].pk,projname)))
        except XML.DoesNotExistError:
            d['message'] = 'XML error, users do not exist.'
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
        try:
            XML.AddUser(enc(d['user'].pk,projname), username)
        except XML.DoesNotExistError:
            d['message'] = 'XML error, users do not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'User already exists in this project.'
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
        try:
            XML.DeleteUser(enc(d['user'].pk,projname), username)
        except XML.DoesNotExistError:
            d['message'] = 'XML error, users do not exist.'
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
        try:
            XML.AddUser(enc(d['user'].pk,projname), newusername)
            XML.DeleteUser(enc(d['user'].pk,projname), oldusername)     # might be changed in the future
        except XML.DoesNotExistError:
            d['message'] = 'XML error, users do not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'User already exists in this project.'
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
        try:
            jsonresponse = json.dumps(XML.GetDNS(enc(d['user'].pk,projname)))
        except XML.DoesNotExistError:
            d['message'] = 'XML error, dnses do not exist.'
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
        try:
            XML.AddDNS(enc(d['user'].pk,projname), dnsname)
        except XML.DoesNotExistError:
            d['message'] = 'XML error, dnses do not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'Dns already exists in this project.'
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
        try:
            XML.DeleteDNS(enc(d['user'].pk,projname), dnsname)
        except XML.DoesNotExistError:
            d['message'] = 'XML error, dnses do not exist.'
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
        try:
            XML.AddDNS(enc(d['user'].pk,projname), newdnsname)
            XML.DeleteDNS(enc(d['user'].pk,projname), olddnsname)     # might be changed in the future
        except XML.DoesNotExistError:
            d['message'] = 'XML error, dnses do not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'Dns already exists in this project.'
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
        try:
            jsonresponse = json.dumps(XML.GetEmail(enc(d['user'].pk,projname)))
        except XML.DoesNotExistError:
            d['message'] = 'XML error, emails do not exist.'
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
        try:
            XML.AddEmail(enc(d['user'].pk,projname), emailname)
        except XML.DoesNotExistError:
            d['message'] = 'XML error, emails do not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'Email already exists in this project.'
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
        try:
            XML.DeleteEmail(enc(d['user'].pk,projname), emailname)
        except XML.DoesNotExistError:
            d['message'] = 'XML error, emails do not exist.'
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
        try:
            XML.AddEmail(enc(d['user'].pk,projname), newemailname)
            XML.DeleteEmail(enc(d['user'].pk,projname), oldemailname)     # might be changed in the future
        except XML.DoesNotExistError:
            d['message'] = 'XML error, emails do not exist.'
        except XML.AlreadyExistsError:
            d['message'] = 'Email already exists in this project.'
        return getEmailData(request)



# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information
