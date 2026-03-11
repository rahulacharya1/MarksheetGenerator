from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import teacher_required


# ---------------- TEACHER DASHBOARD ----------------
@login_required
@teacher_required
def teacherDashboard(request):

    teacher = request.teacher
    classroom = teacher.classroom

    return render(request, "institute/teacher_admin/dashboard.html", {
        "teacher": teacher,
        "classroom": classroom
    })


# ---------------- MANAGE SUBJECTS ----------------
@login_required
@teacher_required
def manageSubjects(request):
    return render(request, "institute/teacher_admin/subjects/manageSubjects.html")
    

# ---------------- ADD SUBJECTS ----------------
@login_required
@teacher_required
def addSubjects(request):

    teacher = request.teacher
    classroom = teacher.classroom
    error = None

    if request.method == "POST":
        subject_name = request.POST.get("subject_name")

        if not subject_name:
            error = "Subject name is required."

        elif ClassSubject.objects.filter(classroom=classroom, subject__iexact=subject_name).exists():
            error = f"{subject_name} is already registered for this class."

        else:
            ClassSubject.objects.create(
                classroom=classroom,
                subject=subject_name.strip()
            )
            return redirect("viewsubjects")

    return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
        "classroom": classroom,
        "error": error
    })
    
    
# ---------------- VIEW SUBJECTS ----------------
@login_required
@teacher_required
def viewSubjects(request):
    
    teacher = request.teacher
    classroom = teacher.classroom
    
    subjects = ClassSubject.objects.filter(classroom=classroom).order_by('subject')

    return render(request, "institute/teacher_admin/subjects/viewSubjects.html", {
        "subjects": subjects,
        "classroom": classroom,
    })
    

# ---------------- MANAGE STUDENTS ----------------
@login_required
@teacher_required
def manageStudents(request):
    return render(request, "institute/teacher_admin/students/manageStudents.html")


# ---------------- ADD STUDENT ----------------
@login_required
@teacher_required
def addStudents(request):

    teacher = request.teacher
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
@teacher_required
def viewStudents(request):
    
    teacher = request.teacher
    classroom = teacher.classroom
    
    students = Student.objects.filter(class_room=classroom).order_by("roll_no")

    return render(request, "institute/teacher_admin/students/viewStudents.html", {
        "students": students,
        "classroom": classroom,
    })  
    
    
# ---------------- MANAGE EXAMS ----------------
@login_required
@teacher_required
def manageExams(request):
    return render(request, "institute/teacher_admin/exams/manageExams.html")


# ---------------- ADD EXAM ----------------
@login_required
@teacher_required
def addExams(request):
    teacher = request.teacher
    classroom = teacher.classroom
    error = None

    if request.method == "POST":
        exam_name = request.POST.get("exam_type", "").strip()

        if not exam_name:
            error = "Exam name is required."

        elif Exam.objects.filter(name__iexact=exam_name, classes=classroom).exists():
            error = f"'{exam_name}' is already created for this class."

        else:
            exam = Exam.objects.create(name=exam_name)
            exam.classes.add(classroom)
            return redirect("viewexams")

    return render(request, "institute/teacher_admin/exams/addExams.html", {
        "error": error
    })


# ---------------- VIEW EXAMS ----------------
@login_required
@teacher_required
def viewExams(request):
    teacher = request.teacher
    classroom = teacher.classroom

    exams = Exam.objects.filter(classes=classroom).order_by('-id')

    context = {
        'classroom': classroom,
        'exams': exams,
        'school': classroom.school,
    }

    return render(request, "institute/teacher_admin/exams/viewExams.html", context)

    
# ---------------- MANAGE MARKS ----------------
@login_required
@teacher_required
def manageMarks(request):
    return render(request, "institute/teacher_admin/marks/manageMarks.html")


# ---------------- ADD MARKS ----------------
@login_required
@teacher_required
def addMarks(request):
    return render(request, "institute/teacher_admin/marks/addmarks.html")


# ---------------- VIEW MARKS ----------------
@login_required
@teacher_required
def viewMarks(request):
    return render(request, "institute/teacher_admin/marks/viewmarks.html")


# ---------------- VIEW RESULT ----------------
@login_required
@teacher_required
def viewResults(request):
    return render(request, "institute/marks/viewresult.html")

