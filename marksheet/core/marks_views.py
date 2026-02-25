from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Sum


# ---------------- MANAGE MARKS ----------------
@login_required
def manageMarks(request):
    return render(request, 'institute/marks/managemarks.html')


# ---------------- ADD MARKS ----------------
@login_required
def addMarks(request):
    school = School.objects.get(user=request.user)

    classes = ClassRoom.objects.filter(school=school)
    subjects = Subject.objects.all()

    selected_class = None
    students = None

    if request.method == "POST":
        class_id = request.POST.get("classroom")
        student_id = request.POST.get("student")

        selected_class = ClassRoom.objects.get(id=class_id)
        student = Student.objects.get(id=student_id)

        for subject in subjects:
            marks_value = request.POST.get(f"marks_{subject.id}")
            if marks_value:
                Mark.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        "marks": marks_value
                    }
                )

        return redirect("viewmarks")

    class_id = request.GET.get("classroom")
    if class_id:
        selected_class = ClassRoom.objects.get(id=class_id)
        students = Student.objects.filter(class_room=selected_class)

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
    school = School.objects.get(user=request.user)

    marks = Mark.objects.filter(
        student__school=school
    ).select_related("student", "subject", "student__class_room").order_by(
        "student__class_room__name",
        "student__class_room__section",
        "student__roll_no"
    )

    return render(request, "institute/marks/viewmarks.html", {"marks": marks})


@login_required
def viewResults(request):
    student_id = request.GET.get("student_id")

    if student_id:
        student = Student.objects.filter(
            id=student_id,
            school__user=request.user
        ).first()

        if student:
            student_marks = Mark.objects.filter(
                student=student
            ).select_related("subject", "student__class_room")

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

            context = {
                "student": student,
                "marks": student_marks,
                "total_obtained": total_obtained,
                "total_possible": total_possible,
                "percentage": percentage,
                "grade": grade,
                "classroom": student.class_room
            }

            return render(request, "institute/marks/viewresult.html", context)

    return redirect("viewmarks")

