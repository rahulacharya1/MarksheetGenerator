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
    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return redirect('dashboard')

    classroom = teacher.classroom

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        pattern = request.POST.get('marks_pattern')

        try:
            theory_max, practical_max = map(int, pattern.split('-'))

            if not ClassSubject.objects.filter(
                classroom=classroom,
                subject=subject_name
            ).exists():
                ClassSubject.objects.create(
                    classroom=classroom,
                    subject=subject_name,
                    full_marks=100,
                    theory_max=theory_max,
                    practical_max=practical_max
                )
                return redirect('viewsubjects')
        except (ValueError, AttributeError):
            pass

    return render(
        request,
        "institute/teacher_admin/subjects/addSubjects.html",
        {'classroom': classroom}
    )


# ---------------- VIEW SUBJECTS ----------------
@login_required
@teacher_required
def viewSubjects(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    subjects = ClassSubject.objects.filter(classroom=teacher.classroom)

    context = {
        'subjects': subjects,
        'classroom': teacher.classroom
    }
    return render(request, "institute/teacher_admin/subjects/viewSubjects.html", context)


# ---------------- EDIT SUBJECTS ----------------
@login_required
@teacher_required
def editSubject(request, subject_id):
    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return redirect('dashboard')

    subject = ClassSubject.objects.filter(
        id=subject_id,
        classroom=teacher.classroom
    ).first()

    if not subject:
        return redirect('viewsubjects')

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        pattern = request.POST.get('marks_pattern')

        try:
            theory_max, practical_max = map(int, pattern.split('-'))

            if not ClassSubject.objects.filter(
                classroom=teacher.classroom,
                subject=subject_name
            ).exclude(id=subject_id).exists():

                subject.subject = subject_name
                subject.theory_max = theory_max
                subject.practical_max = practical_max
                subject.save()

                return redirect('viewsubjects')
        except (ValueError, AttributeError):
            pass

    current_pattern = f"{subject.theory_max}-{subject.practical_max}"

    return render(
        request,
        "institute/teacher_admin/subjects/addSubjects.html",
        {
            'subject': subject,
            'classroom': teacher.classroom,
            'is_edit': True,
            'current_pattern': current_pattern
        }
    )


# ---------------- DELETE SUBJECTS ----------------
@login_required
@teacher_required
def deleteSubject(request, subject_id):
    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return redirect('dashboard')

    subject = ClassSubject.objects.filter(
        id=subject_id,
        classroom=teacher.classroom
    ).first()

    if subject:
        subject.delete()

    return redirect('viewsubjects')
    

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
    
# ---------------- MANAGE MARKS ----------------
@login_required
@teacher_required
def manageMarks(request):
    return render(request, "institute/teacher_admin/marks/manageMarks.html")


# ---------------- ADD MARKS ----------------
@login_required
@teacher_required
def addMarks(request):
    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return redirect('dashboard')

    classroom = teacher.classroom
    subjects = ClassSubject.objects.filter(classroom=classroom)
    students = Student.objects.filter(class_room=classroom).order_by('roll_no')

    if request.method == "POST":
        student_id = request.POST.get('student')
        exam_type = request.POST.get('exam')

        if not student_id or not exam_type:
            return redirect('addmarks')

        student = Student.objects.filter(
            id=student_id,
            class_room=classroom
        ).first()

        if not student:
            return redirect('addmarks')

        for subject in subjects:
            theory = request.POST.get(f'theory_{subject.id}', 0)
            practical = request.POST.get(f'practical_{subject.id}', 0)

            theory = int(theory) if theory else 0
            practical = int(practical) if practical else 0

            Mark.objects.update_or_create(
                student=student,
                subject=subject,
                exam=exam_type,
                defaults={
                    'theory_marks': theory,
                    'practical_marks': practical
                }
            )

        return redirect('viewmarks')

    return render(
        request,
        "institute/teacher_admin/marks/addMarks.html",
        {
            'subjects': subjects,
            'students': students,
            'classroom': classroom
        }
    )


# ---------------- VIEW MARKS ----------------
@login_required
@teacher_required
def viewMarks(request):
    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return redirect('dashboard')

    selected_exam = request.GET.get('exam', 'Final')

    marks = Mark.objects.filter(
        student__class_room=teacher.classroom,
        exam=selected_exam
    ).select_related('student', 'subject', 'student__class_room')

    return render(
        request,
        "institute/teacher_admin/marks/viewmarks.html",
        {
            'marks': marks,
            'selected_exam': selected_exam,
            'classroom': teacher.classroom,
        }
    )


# ---------------- VIEW RESULTS ----------------
@login_required
@teacher_required
def viewResults(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        return redirect('dashboard')

    student_id = request.GET.get('student_id')
    selected_exam = request.GET.get('exam', 'Final')

    student = Student.objects.filter(
        id=student_id,
        class_room=teacher.classroom
    ).first()

    if not student:
        return redirect('viewmarks')

    marks = Mark.objects.filter(student=student, exam=selected_exam).select_related('subject')

    total_obtained = sum(m.total_marks() for m in marks)
    total_subjects = marks.count()
    total_possible = total_subjects * 100

    percentage = round((total_obtained / total_possible) * 100, 2) if total_possible > 0 else 0

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
        'student': student,
        'classroom': teacher.classroom,
        'marks': marks,
        'total_obtained': total_obtained,
        'total_possible': total_possible,
        'percentage': percentage,
        'grade': grade,
        'selected_exam': selected_exam,
    }

    return render(request, "institute/teacher_admin/marks/viewResult.html", context)