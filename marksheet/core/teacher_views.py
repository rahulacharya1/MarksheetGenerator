from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import *
from django.contrib import messages


# ---------------- TEACHER DASHBOARD ----------------
@login_required
def teacherDashboard(request):

    if not hasattr(request.user, "teacher"):
        return redirect("home")

    teacher = request.user.teacher
    classroom = teacher.classroom

    return render(request, "institute/teacher_admin/dashboard.html", {
        "teacher": teacher,
        "classroom": classroom
    })


# ---------------- MANAGE SUBJECTS ----------------
@login_required
def manageSubjects(request):
    return render(request, "institute/teacher_admin/subjects/manageSubjects.html")
    

# ---------------- ADD SUBJECTS ----------------
@login_required
def addSubjects(request):
    teacher_profile = Teacher.objects.get(user=request.user)
    classroom = teacher_profile.classroom
    
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")

        if not subject_name:
            messages.error(request, "Subject name is required.")
            return redirect("addsubjects")

        if ClassSubject.objects.filter(classroom=classroom, subject__iexact=subject_name).exists():
            messages.error(request, f"'{subject_name}' is already registered for this class.")
        else:
            ClassSubject.objects.create(
                classroom=classroom,
                subject=subject_name.strip()
            )
            messages.success(request, f"Subject '{subject_name}' initialized successfully.")
            return redirect("viewsubjects")

    return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
        "classroom": classroom
    })
    
    
# ---------------- VIEW SUBJECTS ----------------
@login_required
def viewSubjects(request):
    teacher_profile = Teacher.objects.get(user=request.user)
    classroom = teacher_profile.classroom
    
    subjects = ClassSubject.objects.filter(classroom=classroom).order_by('subject')

    return render(request, "institute/teacher_admin/subjects/viewSubjects.html", {
        "subjects": subjects,
        "classroom": classroom,
    })
    

# ---------------- MANAGE STUDENTS ----------------
@login_required
def manageStudents(request):
    return render(request, "institute/teacher_admin/students/manageStudents.html")


# ---------------- ADD STUDENT ----------------
@login_required
def addStudents(request):

    if not hasattr(request.user, "teacher"):
        return redirect("viewstudents")

    teacher = request.user.teacher
    school = teacher.school
    classroom = teacher.classroom

    if request.method == "POST":

        studentname = request.POST.get("studentname")
        roll = request.POST.get("roll")
        dob = request.POST.get("dob")

        if Student.objects.filter(
            class_room=classroom,
            roll_no=roll
        ).exists():

            return render(request, "institute/teacher_admin/students/addstudents.html", {
                "classroom": classroom,
                "school": school,
                "error": "Roll number already exists in this class."
            })

        Student.objects.create(
            school=school,
            class_room=classroom,
            student_name=studentname,
            roll_no=roll,
            dob=dob
        )

        return redirect("viewstudents")

    return render(request, "institute/teacher_admin/students/addstudents.html", {
        "classroom": classroom,
        "school": school
    })

# ---------------- VIEW STUDENTS ----------------
@login_required
def viewStudents(request):
    
    teacher_profile = Teacher.objects.get(user=request.user)
    classroom = teacher_profile.classroom
    
    students = Student.objects.filter(class_room=teacher_profile.classroom).order_by("roll_no")

    return render(request, "institute/teacher_admin/students/viewStudents.html", {
        "students": students,
        "classroom": classroom,
    })  
    
    
# ---------------- MANAGE MARKS ----------------
@login_required
def manageMarks(request):
    return render(request, "institute/teacher_admin/marks/manageMarks.html")


# ---------------- ADD MARKS ----------------
@login_required
def addMarks(request):

    if not hasattr(request.user, "teacher"):
        return redirect("viewmarks")

    teacher = request.user.teacher
    classroom = teacher.classroom

    students = Student.objects.filter(class_room=classroom)
    exams = Exam.objects.all()
    
    subject = ClassSubject.objects.all()

    if request.method == "POST":

        student_id = request.POST.get("student")
        exam_id = request.POST.get("exam")
        marks_value = request.POST.get("marks")

        student = Student.objects.get(id=student_id, class_room=classroom)
        exam = Exam.objects.get(id=exam_id)

        Mark.objects.update_or_create(
            student=student,
            exam=exam,
            defaults={"marks": marks_value}
        )

        return redirect("viewmarks")

    return render(request, "institute/teacher_admin/marks/addmarks.html", {
        "students": students,
        "exams": exams,
        "classroom": classroom,
        "subjects": subject
    })


# ---------------- VIEW MARKS ----------------
@login_required
def viewMarks(request):

    # Principal
    if hasattr(request.user, "school"):

        school = request.user.school

        marks = Mark.objects.filter(
            student__school=school
        )

    # Teacher
    elif hasattr(request.user, "teacher"):

        teacher = request.user.teacher

        marks = Mark.objects.filter(
            student__class_room=teacher.classroom
        )

    else:
        return redirect("home")

    marks = marks.select_related(
        "student",
        "exam"
    ).order_by(
        "student__class_room__name",
        "student__roll_no"
    )

    return render(request, "institute/teacher_admin/marks/viewmarks.html", {
        "marks": marks
    })


# ---------------- VIEW RESULT ----------------
@login_required
def viewResults(request):

    student_id = request.GET.get("student_id")

    if not student_id:
        return redirect("viewmarks")

    student = Student.objects.filter(id=student_id).first()

    if not student:
        return redirect("viewmarks")

    marks = Mark.objects.filter(
        student=student
    ).select_related("exam")

    total_obtained = marks.aggregate(Sum('marks'))['marks__sum'] or 0
    total_possible = marks.count() * 100

    percentage = 0
    if total_possible > 0:
        percentage = round((total_obtained / total_possible) * 100, 1)

    # Grade system
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

    return render(request, "institute/marks/viewresult.html", {
        "student": student,
        "marks": marks,
        "total_obtained": total_obtained,
        "total_possible": total_possible,
        "percentage": percentage,
        "grade": grade,
        "classroom": student.class_room
    })

