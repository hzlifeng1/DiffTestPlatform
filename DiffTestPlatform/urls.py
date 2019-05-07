"""DiffTestPlatform URL Configuration

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
from CodeDiff import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('register/',views.register),
    path('index/',views.index),
    path('index/<int:eid>/',views.index),
    path('task_search/<int:eid>/',views.task_search),
    path('task_search/',views.task_search),
    path('edit_task/<int:eid>/<int:tid>/',views.edit_task),
    path('add_task/<int:eid>/',views.add_task),
    path('add_task/', views.add_task),
    path('jacoco_diff/<int:eid>/<int:tid>/',views.jacoco_diff),
    path('diff_report/<int:eid>/<task>/<package>/<class_name>/',views.diff_report,name='detail')
]
