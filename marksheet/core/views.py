from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.db.models import Sum


# ---------------- HOME ----------------
def home(request):
    return render(request, "home.html")


# ---------------- STATE SELECTION ----------------
def state(request):
    type_param = request.GET.get('type')
    states = States.objects.all()
    return render(request, "state.html", {
        "states": states,
        "type": type_param
    })


# ---------------- LOGIN ----------------
def loginView(request):
    state_id = request.GET.get('state')
    state = None
    if state_id:
        try:
            state = States.objects.get(id=state_id)
        except States.DoesNotExist:
            return redirect('state')

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, "institute/login.html", {
        "state": state
    })


# ---------------- REGISTER ----------------
def registerView(request):
    state_id = request.GET.get('state')
    if not state_id:
        return redirect('state')

    try:
        state = States.objects.get(id=state_id)
    except States.DoesNotExist:
        return redirect('state')

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        newUser = User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password,
            email=email
        )

        Schools.objects.create(
            state=state,
            user=newUser,
            name=first_name,
        )

        login(request, newUser)
        return redirect('dashboard')

    return render(request, "institute/register.html", {
        "state": state
    })


# ---------------- LOGOUT ----------------
def logoutView(request):
    logout(request)
    return redirect('home')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    school = Schools.objects.get(user=request.user)
    state = school.state
    return render(request, "institute/dashboard.html", {
        "school": school,
        "state": state
    })


# ---------------- PROFILE ----------------
@login_required
def institutionProfile(request):
    school = Schools.objects.get(user=request.user)
    return render(request, "institute/profile.html", {"school": school})


# ---------------- ABOUT US ----------------
def aboutUs(request):
    return render(request, 'about.html')


# ---------------- DOCUMENTATION ----------------
def documentation(request):
    return render(request, 'institute/documentation.html')


# ---------------- RESULT ----------------
def result(request):
    state_id = request.GET.get("state")

    if not state_id:
        return redirect("state")

    schools = Schools.objects.filter(state_id=state_id)

    school_id = request.GET.get("school")
    class_id = request.GET.get("classroom")

    classrooms = None
    students = None

    if school_id:
        classrooms = ClassRoom.objects.filter(school_id=school_id)

    if class_id:
        students = Students.objects.filter(class_room_id=class_id)

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
    student_id = request.POST.get("roll_no")

    student = Students.objects.filter(
        id=student_id,
        school__state_id=state_id
    ).first()

    if not student:
        return redirect("state")

    student_marks = Marks.objects.filter(
        student=student
    ).select_related("subject")

    total_obtained = student_marks.aggregate(Sum('marks'))['marks__sum'] or 0
    total_possible = student_marks.count() * 100
    percentage = (total_obtained / total_possible * 100) if total_possible > 0 else 0
    percentage = round(percentage, 1)

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
