from django.contrib import admin
from django.urls import path
from core.views import *
from core.admin_views import *
from core.teacher_views import *
from core.principal_views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', home, name='home'),
    path('state/', state, name='state'),
    
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    
    path('about-us/', aboutUs, name='aboutus'),
    path('documentation/', documentation, name='documentation'),
    
    path('admin-approval/', approval, name='adminapproval'),
    
    path('result/', result, name='result'),
    path('show-result/', showResult, name='showresult'),
    
    # ---------------- PRINCIPAL ADMIN ----------------
    
    path('principal-dashboard/', principalDashboard, name='principaldashboard'),
    path('academic-year/', academicYear, name="academicyear"),
    path('profile/', institutionProfile, name='profile'),
    
    path('manage-class/', manageClass, name="manageclass"),
    path('add-class/', addClass, name="addclass"),
    path('view-class/', viewClass, name="viewclass"),
    
    path("manage-teachers/", manageTeachers, name="manageteachers"),
    path("add-teachers/", addTeachers, name="addteachers"),
    path("view-teachers/", viewTeachers, name="viewteachers"),
    
    # ---------------- TEACHER ADMIN ----------------
    
    path('teacher-dashboard/', teacherDashboard, name="teacherdashboard"),
    
    path('manage-exams/', manageExams, name="manageexams"),
    path('add-exams/', addExams, name="addexams"),
    path('view-exams/', viewExams, name="viewexams"),
    
    path('manage-subjects/', manageSubjects, name="managesubjects"),
    path('add-subjects/', addSubjects, name="addsubjects"),
    path('view-subjects/', viewSubjects, name="viewsubjects"),
    
    path('manage-students/', manageStudents, name="managestudents"),
    path('add-students/', addStudents, name="addstudents"),
    path('view-students/', viewStudents, name="viewstudents"),
    
    path('manage-marks/', manageMarks, name="managemarks"),
    path('add-marks/', addMarks, name="addmarks"),
    path('view-marks/', viewMarks, name="viewmarks"),
    path('view-results/', viewResults, name="viewresults"),
    
    # ---------------- ADMIN ----------------
    
    path('admin-dashboard', adminDashboard, name="admindashboard"),
    
    path('add-state', addState, name="addstate"),
    path('view-state', viewState, name="viewstate"),
    
    path('view-institute', viewInstitute, name="viewinstitute"),
    
    path("admin/school/approve/<int:school_id>/", approveSchool, name="approveschool"),
    path("admin/school/remove/<int:school_id>/", removeSchool, name="removeschool"),
    path("admin/school/delete/<int:school_id>/", deleteSchool, name="deleteschool"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
