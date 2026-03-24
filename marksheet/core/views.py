from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# ---------------- HOME ----------------
def home(request):
    return render(request, "home.html")


# ---------------- STATE SELECTION ----------------
def state(request):
    type_param = request.GET.get('type')
    states = State.objects.all()

    return render(request, "state.html", {
        "states": states,
        "type": type_param
    })


# ---------------- LOGIN ----------------
def loginView(request):

    state_id = request.GET.get('state')

    if not state_id:
        return redirect('state')

    state = State.objects.filter(id=state_id).first()

    if not state:
        return redirect('state')

    if request.method == "POST":

        user = authenticate(
            request,
            username = request.POST.get('username'),
            password = request.POST.get('password')
        )

        if user and user.is_active:

            # ---------- PRINCIPAL LOGIN ----------
            school = School.objects.filter(user=user).first()

            if school:

                if str(school.state.id) != str(state_id):
                    return render(request, "institute/login.html", {
                        "state": state,
                        "error": "Invalid state for this school account."
                    })

                if not school.is_verified:
                    return redirect('adminapproval')

                login(request, user)
                return redirect("principaldashboard")

            # ---------- TEACHER LOGIN ----------
            teacher = Teacher.objects.filter(user=user).first()
            
            if teacher:

                if str(teacher.school.state.id) != str(state_id):
                    return render(request, "institute/login.html", {
                        "state": state,
                        "error": "Invalid state for this teacher account."
                    })

                login(request, user)
                return redirect("teacherdashboard")

        return render(request, "institute/login.html", {
            "state": state,
            "error": "Invalid username or password"
        })

    return render(request, "institute/login.html", {
        "state": state,
        "type": "institute"
    })


# ---------------- REGISTER ----------------
def registerView(request):

    state_id = request.GET.get('state')

    if not state_id:
        return redirect('state')

    state = State.objects.filter(id=state_id).first()

    if not state:
        return redirect('state')

    if request.method == "POST":

        school_name = request.POST.get("school_name")
        established_year = request.POST.get("established_year")
        board = request.POST.get("board")
        affiliation_number = request.POST.get("affiliation_number")

        email = request.POST.get("official_email")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")

        admin_name = request.POST.get("admin_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        registration_certificate = request.FILES.get("registration_certificate")
        logo = request.FILES.get('logo')

        current_year = datetime.now().year

        if password != confirm_password:
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Passwords do not match"
            })

        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$', password):
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Password must be at least 8 characters with 1 capital, 1 number, and 1 special character"
            })

        if established_year:
            try:
                established_year = int(established_year)
                if established_year < 1900 or established_year > current_year:
                    raise ValueError
            except:
                return render(request, "institute/register.html", {
                    "state": state,
                    "error": "Invalid established year"
                })

        try:
            validate_email(email)
        except ValidationError:
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Invalid email format"
            })

        if not re.match(r'^[6-9]\d{9}$', phone):
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Enter valid 10-digit Indian phone number"
            })

        if not re.match(r'^\d{6}$', pincode):
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Pincode must be 6 digits"
            })

        if affiliation_number:
            if not re.match(r'^[A-Za-z0-9\-]+$', affiliation_number):
                return render(request, "institute/register.html", {
                    "state": state,
                    "error": "Invalid affiliation number"
                })

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Username can only contain letters, numbers, underscore"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Username already exists"
            })

        if School.objects.filter(official_email=email).exists():
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Official email already registered"
            })

        user = User.objects.create_user(
            username=username.lower(),
            password=password,
            email=email.lower(),
            first_name=admin_name
        )

        School.objects.create(
            user=user,
            school_name=school_name,
            established_year=established_year if established_year else None,
            board=board,
            affiliation_number=affiliation_number,
            official_email=email.lower(),
            phone=phone,
            state=state,
            pincode=pincode,
            registration_certificate=registration_certificate,
            logo=logo
        )

        return redirect('adminapproval')

    return render(request, "institute/register.html", {
        "state": state,
        "type": "register"
    })


# ---------------- LOGOUT ----------------
def logoutView(request):
    logout(request)
    return redirect('home')


# ---------------- ABOUT ----------------
def aboutUs(request):
    return render(request, 'about.html')


# ---------------- DOCUMENTATION ----------------
def documentation(request):
    return render(request, 'institute/documentation.html')


# ---------------- APPROVAL ----------------
def approval(request):
    return render(request, "institute/adminapproval.html")


# ---------------- RESULT ----------------
def result(request):
    state_id = request.GET.get("state")
    if not state_id:
        return redirect("state")

    schools = School.objects.filter(state_id=state_id, is_verified=True)
    school_id = request.GET.get("school")

    return render(request, "result.html", {
        "schools": schools,
        "state_id": state_id,
        "school_id": school_id,
    })


# ---------------- SHOW RESULT ----------------
def showResult(request):
    if request.method != "POST":
        return redirect("result")

    school_id = request.POST.get("school_id")
    state_id = request.POST.get("state_id")
    grade = request.POST.get("grade")
    section = request.POST.get("section")
    roll_no = request.POST.get("roll_no")
    dob_input = request.POST.get("dob")
    exam_type = request.POST.get("exam")

    schools = School.objects.filter(state_id=state_id, is_verified=True)

    if not all([school_id, grade, section, roll_no, dob_input, exam_type]):
        return render(request, "result.html", {
            "error": "All fields are required",
            "state_id": state_id,
            "school_id": school_id,
            "grade": grade,
            "section": section,
            "roll_no": roll_no,
            "dob": dob_input,
            "exam": exam_type,
            "schools": schools
        })

    try:
        dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
    except ValueError:
        return render(request, "result.html", {
            "error": "Invalid date format",
            "state_id": state_id,
            "school_id": school_id,
            "grade": grade,
            "section": section,
            "roll_no": roll_no,
            "dob": dob_input,
            "exam": exam_type,
            "schools": schools
        })

    classroom = ClassRoom.objects.filter(
        school_id=school_id,
        name=grade,
        section=section.upper()
    ).first()

    if not classroom:
        return render(request, "result.html", {
            "error": "Invalid class or section",
            "state_id": state_id,
            "school_id": school_id,
            "grade": grade,
            "section": section,
            "roll_no": roll_no,
            "dob": dob_input,
            "exam": exam_type,
            "schools": schools
        })

    student = Student.objects.filter(
        class_room=classroom,
        roll_no=roll_no,
        dob=dob
    ).first()

    if not student:
        return render(request, "result.html", {
            "error": "Student not found. Check Roll No & DOB.",
            "state_id": state_id,
            "school_id": school_id,
            "grade": grade,
            "section": section,
            "roll_no": roll_no,
            "dob": dob_input,
            "exam": exam_type,
            "schools": schools
        })

    marks = Mark.objects.filter(
        student=student,
        exam=exam_type
    ).select_related("subject")

    if not marks.exists():
        return render(request, "result.html", {
            "error": "Result not uploaded yet",
            "state_id": state_id,
            "school_id": school_id,
            "grade": grade,
            "section": section,
            "roll_no": roll_no,
            "dob": dob_input,
            "exam": exam_type,
            "schools": schools
        })

    total_obtained = sum(m.total_marks() for m in marks)
    total_possible = sum(m.subject.theory_max + m.subject.practical_max for m in marks)

    percentage = round((total_obtained / total_possible) * 100, 1) if total_possible > 0 else 0

    if percentage >= 90: final_grade = "A+"
    elif percentage >= 80: final_grade = "A"
    elif percentage >= 70: final_grade = "B"
    elif percentage >= 60: final_grade = "C"
    elif percentage >= 50: final_grade = "D"
    elif percentage >= 35: final_grade = "E"
    else: final_grade = "F"

    return render(request, "showResult.html", {
        "student": student,
        "marks": marks,
        "total_obtained": total_obtained,
        "total_possible": total_possible,
        "percentage": percentage,
        "grade": final_grade,
        "exam_type": exam_type
    })
    
