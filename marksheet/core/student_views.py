from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Schools, ClassRoom, Students


# ---------------- MANAGE STUDENTS ----------------
@login_required
def manageStudents(request):
    return render(request, 'institute/students/managestudents.html')


# ---------------- ADD STUDENT ----------------
@login_required
def addStudents(request):
    try:
        school = Schools.objects.get(user=request.user)
    except Schools.DoesNotExist:
        return redirect('dashboard')

    classrooms = ClassRoom.objects.filter(school=school)

    if request.method == "POST":
        classroom_id = request.POST.get("classroom")
        studentname = request.POST.get("studentname")
        roll = request.POST.get("roll")
        dob = request.POST.get("dob")

        roll_exists = Students.objects.filter(
            school=school,
            class_room_id=classroom_id,
            roll_no=roll
        ).exists()

        if roll_exists:
            return render(request, "institute/students/addstudents.html", {
                "classrooms": classrooms
            })

        classroom = ClassRoom.objects.get(
            id=classroom_id,
            school=school
        )

        Students.objects.create(
            school=school,
            class_room=classroom,
            studentName=studentname,
            roll_no=roll,
            dob=dob
        )

        return redirect('viewstudents')

    return render(request, "institute/students/addstudents.html", {
        "classrooms": classrooms
    })


# ---------------- VIEW STUDENT ----------------
@login_required
def viewStudents(request):
    school = Schools.objects.get(user=request.user)
    
    students = Students.objects.filter(school=school).order_by(
        'class_room__name', 
        'class_room__section', 
        'roll_no'
    )

    return render(request, "institute/students/viewstudents.html", {
        "students": students,
        "school": school
    })
    
