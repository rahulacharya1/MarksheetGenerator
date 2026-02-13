from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


# ---------------- MANAGE MARKS ----------------
@login_required
def manageMarks(request):
    return render(request, 'institute/marks/managemarks.html')


# ---------------- ADD MARKS ----------------
@login_required
def addMarks(request):
    school = Schools.objects.get(user=request.user)

    classes = ClassRoom.objects.filter(school=school)
    subjects = Subjects.objects.all()

    selected_class = None
    students = None

    if request.method == "POST":
        class_id = request.POST.get("classroom")
        student_id = request.POST.get("student")

        selected_class = ClassRoom.objects.get(id=class_id)
        student = Students.objects.get(id=student_id)

        for subject in subjects:
            marks_value = request.POST.get(f"marks_{subject.id}")
            if marks_value:
                Marks.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        "classroom": selected_class,
                        "marks": marks_value
                    }
                )

        return redirect("viewmarks")

    class_id = request.GET.get("classroom")
    if class_id:
        selected_class = ClassRoom.objects.get(id=class_id)
        students = Students.objects.filter(class_room=selected_class)

    context = {
        "classes": classes,
        "students": students,
        "subjects": subjects,
        "selected_class": selected_class
    }

    return render(request, "institute/marks/addmarks.html", context)


# ---------------- VIEW MARKS ----------------
@login_required
def viewMarks(request):
    school = Schools.objects.get(user=request.user)

    marks = Marks.objects.filter(
        student__school=school
    ).select_related("student", "subject", "classroom")

    return render(request, "institute/marks/viewmarks.html", {"marks": marks})

