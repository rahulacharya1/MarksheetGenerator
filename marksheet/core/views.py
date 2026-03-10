from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import *


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
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:

            # ---------- PRINCIPAL LOGIN ----------
            if hasattr(user, "school"):

                school = user.school

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
            if hasattr(user, "teacher"):

                teacher = user.teacher

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
        "state": state
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

        if password != confirm_password:
            return render(request, "institute/register.html", {
                "state": state,
                "error": "Passwords do not match"
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
            username=username,
            password=password,
            email=email,
            first_name=admin_name
        )

        School.objects.create(
            user=user,
            school_name=school_name,
            established_year=established_year if established_year else None,
            board=board,
            affiliation_number=affiliation_number,
            official_email=email,
            phone=phone,
            state=state,
            pincode=pincode,
            registration_certificate=registration_certificate
        )

        return redirect('adminapproval')

    return render(request, "institute/register.html", {"state": state})


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

    schools = School.objects.filter(state_id=state_id)

    school_id = request.GET.get("school")
    class_id = request.GET.get("classroom")

    classrooms = None
    students = None

    if school_id:
        classrooms = ClassRoom.objects.filter(school_id=school_id)

    if class_id:
        students = Student.objects.filter(class_room_id=class_id)

    return render(request, "result.html", {
        "schools": schools,
        "classrooms": classrooms,
        "students": students,
        "state_id": state_id,
        "school_id": school_id,
        "class_id": class_id,
    })


# ---------------- SHOW RESULT ----------------
def showResult(request):

    if request.method != "POST":
        return redirect("state")

    state_id = request.POST.get("state_id")
    school_id = request.POST.get("school_id")
    class_id = request.POST.get("class_id")
    student_id = request.POST.get("roll_no")

    student = Student.objects.filter(
        id=student_id,
        school__state_id=state_id,
        class_room_id=class_id
    ).first()

    if not student:
        return redirect("result")

    student_marks = Mark.objects.filter(
        student=student
    ).select_related("exam")

    total_obtained = student_marks.aggregate(Sum('marks'))['marks__sum'] or 0
    total_possible = student_marks.count() * 100

    percentage = 0
    if total_possible > 0:
        percentage = round((total_obtained / total_possible) * 100, 1)

    # -------- GRADE SYSTEM --------
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    elif percentage >= 35:
        grade = "E"
    else:
        grade = "F"

    return render(request, "showResult.html", {
        "student": student,
        "marks": student_marks,
        "total_obtained": total_obtained,
        "total_possible": total_possible,
        "percentage": percentage,
        "grade": grade,
    })
