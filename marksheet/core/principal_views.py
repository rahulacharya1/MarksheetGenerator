from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .decorators import school_required


# ---------------- PRINCIPAL DASHBOARD ----------------
@login_required
@school_required
def principalDashboard(request):

    if not hasattr(request.user, "school"):
        return redirect("home")

    school = request.user.school
    state = school.state
    

    return render(request, "institute/principal_admin/dashboard.html", {
            "school": school,
            "state": state
        }
    )


# ---------------- PROFILE ----------------
@login_required
@school_required
def institutionProfile(request):

    if not hasattr(request.user, "school"):
        return redirect("home")

    school = request.user.school

    return render(
        request,
        "institute/principal_admin/profile.html",
        {"school": school}
    )


# ---------------- ACADEMIC YEAR ----------------
@login_required
@school_required
def academicYear(request):

    if not hasattr(request.user, "school"):
        return redirect("home")

    school = request.user.school

    if request.method == "POST":
        year = request.POST.get("year")

        if year:
            AcademicYear.objects.create(
                school=school,
                year=year
            )

        return redirect("academicyear")

    years = AcademicYear.objects.filter(school=school)

    return render(
        request,
        "institute/principal_admin/academicYear.html",
        {"years": years}
    )


# ---------------- MANAGE CLASS ----------------
@login_required
@school_required
def manageClass(request):

    school = request.user.school

    return render(
        request,
        "institute/principal_admin/class/manageclass.html",
        {"school": school}
    )


# ---------------- ADD CLASS ----------------
@login_required
@school_required
def addClass(request):

    school = request.user.school
    academic_years = AcademicYear.objects.filter(school=school)

    if request.method == "POST":

        classname = request.POST.get("classname")
        section = request.POST.get("section")
        year_id = request.POST.get("academic_year")

        # Validate class number
        try:
            classname = int(classname)
        except (ValueError, TypeError):
            return render(
                request,
                "institute/principal_admin/class/addclass.html",
                {
                    "school": school,
                    "academic_years": academic_years,
                    "error": "Class must be a number between 1 and 12."
                }
            )

        if classname < 1 or classname > 12:
            return render(
                request,
                "institute/principal_admin/class/addclass.html",
                {
                    "school": school,
                    "academic_years": academic_years,
                    "error": "Class must be between 1 and 12 only."
                }
            )

        # Validate section
        if section not in ["A", "B", "C"]:
            return render(
                request,
                "institute/principal_admin/class/addclass.html",
                {
                    "school": school,
                    "academic_years": academic_years,
                    "error": "Section must be A, B or C only."
                }
            )

        # Validate academic year
        if not year_id:
            return render(
                request,
                "institute/principal_admin/class/addclass.html",
                {
                    "school": school,
                    "academic_years": academic_years,
                    "error": "Please select academic year."
                }
            )

        academic_year = AcademicYear.objects.get(
            id=year_id,
            school=school
        )

        # Prevent duplicate class
        if ClassRoom.objects.filter(
            school=school,
            academic_year=academic_year,
            name=classname,
            section=section
        ).exists():

            return render(
                request,
                "institute/principal_admin/class/addclass.html",
                {
                    "school": school,
                    "academic_years": academic_years,
                    "error": "This class already exists for this academic year."
                }
            )

        # Create class
        ClassRoom.objects.create(
            school=school,
            academic_year=academic_year,
            name=classname,
            section=section
        )

        return redirect("viewclass")

    return render(
        request,
        "institute/principal_admin/class/addclass.html",
        {
            "school": school,
            "academic_years": academic_years
        }
    )


# ---------------- VIEW CLASS ----------------
@login_required
@school_required
def viewClass(request):
    school = request.user.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')
    selected_year_id = request.GET.get('year')
    selected_year = None

    if selected_year_id:
        try:
            selected_year = academic_years.get(id=selected_year_id)
        except (AcademicYear.DoesNotExist, ValueError):
            selected_year = academic_years.first()
    else:
        selected_year = academic_years.first()

    classroom_qs = ClassRoom.objects.filter(school=school)
    
    if selected_year:
        classroom_qs = classroom_qs.filter(academic_year=selected_year)

    classroom = classroom_qs.select_related("academic_year").order_by(
        "name",
        "section"
    )

    return render(request, "institute/principal_admin/class/viewclass.html", {
        "allclass": classroom,
        "school": school,
        "academic_years": academic_years,
        "selected_year": selected_year
    })


# ---------------- MANAGE TEACHERS ----------------
@login_required
@school_required
def manageTeachers(request):
    return render( request, "institute/principal_admin/teacher/manageTeacher.html")


# ---------------- ADD TEACHERS ----------------
@login_required
@school_required
def addTeachers(request):
    school = request.user.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')
    
    selected_year_id = request.GET.get('year_filter')
    classrooms = None
    selected_year = None

    if selected_year_id:
        selected_year = academic_years.filter(id=selected_year_id).first()
        if selected_year:
            classrooms = ClassRoom.objects.filter(
                school=school, 
                academic_year=selected_year,
                teacher__isnull=True
            )

    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        classroom_id = request.POST.get("classroom")

        if User.objects.filter(username=username).exists():
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "Username already exists",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year,
                "school": school
            })

        if Teacher.objects.filter(classroom_id=classroom_id).exists():
            return render(request, "institute/principal_admin/teacher/addTeacher.html", {
                "error": "This class has just been assigned to another teacher.",
                "academic_years": academic_years,
                "classrooms": classrooms,
                "selected_year": selected_year,
                "school": school
            })

        user = User.objects.create_user(username=username, password=password, first_name=name)
        classroom = ClassRoom.objects.get(id=classroom_id, school=school)
        
        Teacher.objects.create(
            user=user, 
            school=school, 
            classroom=classroom
        )
        return redirect("viewteachers")

    return render(request, "institute/principal_admin/teacher/addTeacher.html", {
        "academic_years": academic_years,
        "classrooms": classrooms,
        "selected_year": selected_year,
        "school": school
    })
    

# ---------------- VIEW TEACHERS ----------------
@login_required
@school_required
def viewTeachers(request):
    school = request.user.school
    academic_years = AcademicYear.objects.filter(school=school).order_by('-year')
    selected_year_id = request.GET.get('year')
    selected_year = None

    if selected_year_id:
        try:
            selected_year = academic_years.get(id=selected_year_id)
        except (AcademicYear.DoesNotExist, ValueError):
            selected_year = academic_years.first()
    else:
        selected_year = academic_years.first()

    teacher_qs = Teacher.objects.filter(school=school).select_related('user', 'classroom')
    
    if selected_year:
        teacher_qs = teacher_qs.filter(classroom__academic_year=selected_year)

    return render(request, "institute/principal_admin/teacher/viewTeacher.html", {
        "teachers": teacher_qs,
        "school": school,
        "academic_years": academic_years,
        "selected_year": selected_year
    })

