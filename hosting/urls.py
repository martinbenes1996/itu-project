"""hosting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hosting import views
#admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name=''),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('info/', views.info, name='info'),
    path('createpage/', views.createpage, name="createpage"),
    path('deletepage/', views.deletepage, name="deletepage"),
    path('renamepage/', views.renamepage, name="renamepage"),
    path('pageboard/', views.pageboard, name='pageboard'),
    path('getDirData/', views.getDirData, name='dirdata'),
    path('createDir/', views.createDir, name='createdir'),
    path('createFile/', views.createFile, name='createfile'),
    path('renameFile/', views.renameFile, name='renamefile'),
    path('deleteFile/', views.deleteFile, name='deletefile'),
    path('getTableNames/', views.getTableNames, name='tablenames'),
    path('getDbData/', views.getDbData, name='dbdata'),
    path('createTable/', views.createTable, name='createtable'),
    path('deleteTable/', views.deleteTable, name='deletetable'),
    path('addRow/', views.addRow, name='addrow'),
    path('editRow/', views.editRow, name='editrow'),
    path('deleteRow/', views.deleteRow, name='deleterow'),
    path('addColumn/', views.addColumn, name='addcolumn'),
    path('deleteColumn/', views.deleteColumn, name='deletecolumn'),
    path('addUser/', views.addUser, name='adduser'),
    path('deleteUser/', views.deleteUser, name='deleteuser'),
    path('renameUser/', views.renameUser, name='renameuser'),
    path('getUserData/', views.getUserData, name='userdata'),
    path('addDns/', views.addDns, name='adddns'),
    path('deleteDns/', views.deleteDns, name='deletedns'),
    path('renameDns/', views.renameDns, name='renamedns'),
    path('getDnsData/', views.getDnsData, name='dnsdata'),
    path('addEmail/', views.addEmail, name='addemail'),
    path('deleteEmail/', views.deleteEmail, name='deleteemail'),
    path('renameEmail/', views.renameEmail, name='renameemail'),
    path('getEmailData/', views.getEmailData, name='emaildata')
    # here add new pages
    # path(keyword, views.function)
]
