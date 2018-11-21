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
    path('pageboard/', views.pageboard, name='pageboard'),
    path('getDirData/', views.getDirData, name='dirdata'),
    path('getDbData/', views.getDbData, name='dbdata')
    # here add new pages
    # path(keyword, views.function)
]
