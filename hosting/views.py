from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from hosting.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
                #d['first_name'] = user.first_name
                #d['last_name'] = user.last_name
                #d['email'] = user.email
                #response = render_to_response("dashboard.html", d, context_instance=RequestContext(request))
                response = redirect('dashboard')
                response.set_cookie('user', d['email'], max_age=7200)
                #response.set_cookie('user', d['email'], max_age = 7200)
                return response
                #request.session['member_id'] = user.id
                #return render(request, 'dashboard.html', {'user': d})
            else:
                d['message'] = 'No user with given email'

        if 'message' in d:
            return render(request, "login.html", d)
    else:
        return render(request, "login.html", {})
    
def dashboard(request):
    email = request.COOKIES.get('user')
    d = dict()
    try:
        u = User.objects.get(email=email)
    except:
        d['message'] = 'Unknown user.'
    else:
        d['email'] = email
        d['first_name'] = u.first_name
        d['last_name'] = u.last_name
    
    return render(request, "dashboard.html", d)

def logout(request):
    response = redirect('')
    response.delete_cookie('user')
    return response




# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information