from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from functools import wraps
from .models import School, Teacher

def school_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            school = School.objects.get(user=request.user)
            
            if not school.is_verified:
                print(f"!!! {school.school_name} is no longer verified. Logging out. !!!")
                logout(request)
                messages.error(request, "Your account is no longer verified. Please contact admin.")
                return redirect('adminapproval') 
            
            request.school = school
            return view_func(request, *args, **kwargs)

        except School.DoesNotExist:
            logout(request)
            return redirect('adminapproval')
            
    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        try:
            teacher = Teacher.objects.get(user=request.user)

            if hasattr(teacher, "is_verified") and not teacher.is_verified:
                logout(request)
                messages.error(request, "Your teacher account is not verified.")
                return redirect("home")

            request.teacher = teacher
            return view_func(request, *args, **kwargs)

        except Teacher.DoesNotExist:
            logout(request)
            messages.error(request, "Teacher access required.")
            return redirect("home")

    return _wrapped_view

