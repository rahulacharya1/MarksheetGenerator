from django.contrib import admin
from django.urls import path
from core.views import *
from core.class_views import *
from core.student_views import *
from core.marks_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('state/', state, name="state"),
    path('result/', result, name="result"),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('register/', registerView, name="register"),
    
    path('dashboard/', dashboard, name="dashboard"),
    
    path('manageclass/', manageClass, name="manageclass"),
    path('addclass/', addclass, name="addclass"),
    path('viewclass/', viewclass, name="viewclass"),
    
    path('managestudents/', manageStudents, name="managestudents"),
    path('addstudents/', addStudents, name="addstudents"),
    path('viewstudents/', viewStudents, name="viewstudents"),
    
    path('managemarks/', manageMarks, name="managemarks"),
    path('addmarks/', addMarks, name="addmarks"),
    path('viewmarks/', viewMarks, name="viewmarks"),
]
