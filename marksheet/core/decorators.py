from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from functools import wraps
from .models import School

def school_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            school = School.objects.get(user=request.user)
            
            # --- THE MISSING LOGIC ---
            # If the admin set is_verified to False, logout the user
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
