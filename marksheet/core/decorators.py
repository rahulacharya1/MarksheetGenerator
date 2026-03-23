from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from functools import wraps
from .models import School, Teacher


# ---------------- SCHOOL REQUIRED ----------------
def school_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            school = School.objects.get(user=request.user)
            
            if not school.is_verified:
                messages.error(request, "Your account is not verified. Please contact admin.")
                return redirect('adminapproval') 
            
            request.school = school
            return view_func(request, *args, **kwargs)

        except School.DoesNotExist:
            messages.error(request, "School access required.")
            return redirect('adminapproval')
            
    return _wrapped_view


# ---------------- TEACHER REQUIRED ----------------
def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            teacher = Teacher.objects.get(user=request.user)

            request.teacher = teacher
            return view_func(request, *args, **kwargs)

        except Teacher.DoesNotExist:
            messages.error(request, "Teacher access required.")
            return redirect("home")

    return _wrapped_view

