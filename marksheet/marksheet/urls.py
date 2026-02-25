from django.contrib import admin
from django.urls import path
from core.views import *
from core.class_views import *
from core.student_views import *
from core.marks_views import *
from core.admin_views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', home, name="home"),
    path('state/', state, name="state"),
    path('result/', result, name="result"),
    path("show-result/", showResult, name="showResult"),

    path('about-us/', aboutUs, name='aboutus'),
    path('documentation/', documentation, name='documentation'),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('register/', registerView, name="register"),
    
    path('adminapproval/', approval, name="adminapproval"),
    
    path('dashboard/', dashboard, name="dashboard"),
    path('profile/', institutionProfile, name='profile'),
    
    path('manageclass/', manageClass, name="manageclass"),
    path('addclass/', addclass, name="addclass"),
    path('viewclass/', viewclass, name="viewclass"),
    
    path('managestudents/', manageStudents, name="managestudents"),
    path('addstudents/', addStudents, name="addstudents"),
    path('viewstudents/', viewStudents, name="viewstudents"),
    
    path('managemarks/', manageMarks, name="managemarks"),
    path('addmarks/', addMarks, name="addmarks"),
    path('viewmarks/', viewMarks, name="viewmarks"),
    path('viewresults/', viewResults, name="viewresults"),
    
    path('admin-dashboard', admin_dashboard, name="admin-dashboard"),
    path('addState', addState, name="addState"),
    path('viewState', viewState, name="viewState"),
    path('addSubject', addSubject, name="addSubject"),
    path('viewSubject', viewSubject, name="viewSubject"),
    
    path('viewInstitute', viewInstitute, name="viewInstitute"),
    path("admin/school/approve/<int:school_id>/", approve_school, name="approve_school"),
    path("admin/school/remove/<int:school_id>/", remove_school, name="remove_school"),
    path("admin/school/delete/<int:school_id>/", delete_school, name="delete_school"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
