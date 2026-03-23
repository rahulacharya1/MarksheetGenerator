from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .decorators import school_required
import re
from datetime import datetime


# ---------------- PRINCIPAL DASHBOARD ----------------
@login_required
@school_required
def principalDashboard(request):
    school = request.school
    return render(request, "institute/principal_admin/dashboard.html", {
        "school": school,
        "state": school.state
    })


# ---------------- PROFILE ----------------
@login_required
@school_required
def institutionProfile(request):
    return render(request, "institute/principal_admin/profile.html",
        {"school": request.school}
    )
    
    
# ---------------- EDIT PROFILE ----------------
@login_required
@school_required
def editProfile(request):
    school = request.school

    if request.method == "POST":
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        affiliation_number = request.POST.get("affiliation_number")
        logo = request.FILES.get("logo")

        if not re.match(r'^[6-9]\d{9}$', phone):
            return render(request, "institute/principal_admin/editProfile.html", {
                "school": school,
                "error": "Enter valid 10-digit Indian phone number"
            })

        if not re.match(r'^\d{6}$', pincode):
            return render(request, "institute/principal_admin/editProfile.html", {
                "school": school,
                "error": "Pincode must be 6 digits"
            })

        if affiliation_number:
            if not re.match(r'^[A-Za-z0-9\-]+$', affiliation_number):
                return render(request, "institute/principal_admin/editProfile.html", {
                    "school": school,
                    "error": "Invalid affiliation number"
                })

        school.phone = phone
        school.pincode = pincode
        school.affiliation_number = affiliation_number

        if logo:
            school.logo = logo

        school.save()
        return redirect("profile")

    return render(request, "institute/principal_admin/editProfile.html", {
        "school": school
    })


# ---------------- ACADEMIC YEAR ----------------
@login_required
@school_required
def academicYear(request):
    school = request.school
    years = AcademicYear.objects.filter(school=school)

    if request.method == "POST":
        year = request.POST.get("year")
        
        if not year:
            return render(request, "institute/principal_admin/academicYear.html", {
                "years": years,
                "error": "Please enter academic year"
            })
    
        current_year = datetime.now().year
    
        if not re.match(r'^\d{4}-\d{4}$', year):
            return render(request, "institute/principal_admin/academicYear.html", {
                "years": AcademicYear.objects.filter(school=school),
                "error": "Invalid format! Use YYYY-YYYY (e.g., 2026-2027)"
            })
    
        start, end = map(int, year.split('-'))
    
        if end != start + 1:
            return render(request, "institute/principal_admin/academicYear.html", {
                "years": AcademicYear.objects.filter(school=school),
                "error": "End year must be next of start year"
            })
    
        if start < current_year - 1 or start > current_year + 1:
            return render(request, "institute/principal_admin/academicYear.html", {
                "years": AcademicYear.objects.filter(school=school),
                "error": f"Only valid years allowed around current session ({current_year})"
            })
    
        if AcademicYear.objects.filter(school=school, year=year).exists():
            return render(request, "institute/principal_admin/academicYear.html", {
                "years": AcademicYear.objects.filter(school=school),
                "error": "This academic year already exists"
            })
    
        AcademicYear.objects.create(school=school, year=year)
        return redirect("academicyear")

    return render( request, "institute/principal_admin/academicYear.html",
        {"years": years}
    )


# ---------------- MANAGE CLASS ----------------
@login_required
@school_required
def manageClass(request):
    return render(request, "institute/principal_admin/class/manageclass.html")


# ---------------- ADD CLASS ----------------
@login_required
@school_required
def addClass(request):
    school = request.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')

    if request.method == "POST":
        classname = request.POST.get("classname")
        section = request.POST.get("section")
        year_id = request.POST.get("academic_year")

        try:
            classname = int(classname)
            if classname < 1 or classname > 12:
                raise ValueError
        except:
            return render(request, "institute/principal_admin/class/addclass.html", {
                "academic_years": academic_years,
                "error": "Class must be between 1 and 12"
            })

        section = section.upper()
        if section not in ["A", "B", "C"]:
            return render(request, "institute/principal_admin/class/addclass.html", {
                "academic_years": academic_years,
                "error": "Section must be A, B or C"
            })

        academic_year = AcademicYear.objects.filter(id=year_id, school=school).first()
        if not academic_year:
            return render(request, "institute/principal_admin/class/addclass.html", {
                "academic_years": academic_years,
                "error": "Invalid academic year"
            })

        if ClassRoom.objects.filter(
            school=school,
            academic_year=academic_year,
            name=classname,
            section=section
        ).exists():
            return render(request, "institute/principal_admin/class/addclass.html", {
                "academic_years": academic_years,
                "error": "Class already exists"
            })

        ClassRoom.objects.create(
            school=school,
            academic_year=academic_year,
            name=classname,
            section=section
        )

        return redirect("viewclass")

    return render(request, "institute/principal_admin/class/addclass.html", {
        "academic_years": academic_years
    })


# ---------------- VIEW CLASS ----------------
@login_required
@school_required
def viewClass(request):
    school = request.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')
    selected_year_id = request.GET.get('year')

    selected_year = academic_years.filter(id=selected_year_id).first() if selected_year_id else academic_years.first()

    classroom = ClassRoom.objects.filter(
        school=school,
        academic_year=selected_year
    ).order_by("name", "section")

    return render(request, "institute/principal_admin/class/viewclass.html", {
        "allclass": classroom,
        "academic_years": academic_years,
        "selected_year": selected_year
    })


# ---------------- MANAGE TEACHERS ----------------
@login_required
@school_required
def manageTeachers(request):
    return render( request, "institute/principal_admin/teacher/manageTeacher.html")


# ---------------- ADD TEACHER ----------------
@login_required
@school_required
def addTeachers(request):
    school = request.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')

    selected_year_id = request.GET.get('year_filter')
    selected_year = academic_years.filter(id=selected_year_id).first()
    classrooms = ClassRoom.objects.filter(
        school=school,
        academic_year=selected_year,
        teacher__isnull=True
    ) if selected_year else None

    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        classroom_id = request.POST.get("classroom")

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "Invalid username",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year
            })

        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#]).{8,}$', password):
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "Weak password",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year
            })

        if User.objects.filter(username=username).exists():
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "Username exists",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year
            })

        classroom = ClassRoom.objects.filter(id=classroom_id, school=school).first()
        if not classroom:
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "Invalid classroom",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year
            })

        if Teacher.objects.filter(classroom=classroom).exists():
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "Teacher already assigned",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year
            })

        user = User.objects.create_user(username=username, password=password, first_name=name)

        Teacher.objects.create(
            user=user,
            school=school,
            classroom=classroom
        )

        return redirect("viewteachers")

    return render(request, "institute/principal_admin/teacher/addTeacher.html", {
        "academic_years": academic_years,
        "classrooms": classrooms,
        "selected_year": selected_year
    })


# ---------------- VIEW TEACHERS ----------------
@login_required
@school_required
def viewTeachers(request):
    school = request.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')

    selected_year_id = request.GET.get('year')
    selected_year = academic_years.filter(id=selected_year_id).first() if selected_year_id else academic_years.first()

    teachers = Teacher.objects.filter(
        school=school,
        classroom__academic_year=selected_year
    ).select_related("user", "classroom")

    return render(request, "institute/principal_admin/teacher/viewTeacher.html", {
        "teachers": teachers,
        "academic_years": academic_years,
        "selected_year": selected_year
    })
    
