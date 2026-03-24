from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import teacher_required
from datetime import datetime
import re


# ---------------- TEACHER DASHBOARD ----------------
@login_required
@teacher_required
def teacherDashboard(request):
    teacher = request.teacher
    return render(request, "institute/teacher_admin/dashboard.html", {
        "teacher": teacher,
        "classroom": teacher.classroom
    })

# ---------------- MANAGE SUBJECTS ----------------
@login_required
@teacher_required
def manageSubjects(request):
    return render(request, "institute/teacher_admin/subjects/manageSubjects.html")
    

# ---------------- ADD SUBJECT ----------------
@login_required
@teacher_required
def addSubjects(request):
    teacher = request.teacher
    classroom = teacher.classroom

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        pattern = request.POST.get('marks_pattern')

        if not subject_name:
            return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
                "error": "Subject name required",
                "classroom": classroom
            })

        try:
            theory_max, practical_max = map(int, pattern.split('-'))

            if theory_max + practical_max != 100:
                raise ValueError

        except (ValueError, AttributeError):
            return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
                "error": "Invalid pattern (must be like 70-30)",
                "classroom": classroom
            })

        if ClassSubject.objects.filter(
            classroom=classroom,
            subject__iexact=subject_name.strip()
        ).exists():
            return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
                "error": "Subject already exists",
                "classroom": classroom
            })

        ClassSubject.objects.create(
            classroom=classroom,
            subject=subject_name.strip(),
            theory_max=theory_max,
            practical_max=practical_max
        )

        return redirect('viewsubjects')

    return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
        "classroom": classroom
    })


# ---------------- VIEW SUBJECTS ----------------
@login_required
@teacher_required
def viewSubjects(request):
    teacher = request.teacher
    subjects = ClassSubject.objects.filter(classroom=teacher.classroom)

    return render(request, "institute/teacher_admin/subjects/viewSubjects.html", {
        "subjects": subjects,
        "classroom": teacher.classroom
    })


# ---------------- EDIT SUBJECTS ----------------
@login_required
@teacher_required
def editSubject(request, subject_id):
    teacher = request.teacher

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
        
        if not subject_name:
            return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
                "error": "Subject name required",
                "subject": subject
            })

        try:
            theory_max, practical_max = map(int, pattern.split('-'))
            
            if theory_max + practical_max != 100:
                raise ValueError
            
        except (ValueError, AttributeError):
            return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
                "error": "Invalid pattern",
                "subject": subject
            })

        if ClassSubject.objects.filter(
            classroom=teacher.classroom,
            subject__iexact=subject_name
        ).exclude(id=subject_id).exists():
            return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
                "error": "Subject already exists",
                "subject": subject
            })

        subject.subject = subject_name.strip()
        subject.theory_max = theory_max
        subject.practical_max = practical_max
        subject.save()

        return redirect('viewsubjects')

    current_pattern = f"{subject.theory_max}-{subject.practical_max}"

    return render(request, "institute/teacher_admin/subjects/addSubjects.html", {
        "subject": subject,
        "is_edit": True,
        "current_pattern": current_pattern
    })


# ---------------- DELETE SUBJECTS ----------------
@login_required
@teacher_required
def deleteSubject(request, subject_id):
    teacher = request.teacher

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
    classroom = teacher.classroom
    school = teacher.school

    if request.method == "POST":
        studentname = request.POST.get("studentname")
        roll = request.POST.get("roll")
        dob_input = request.POST.get("dob")
        father_name = request.POST.get("father_name")
        guardian_phone = request.POST.get("guardian_phone")
        address = request.POST.get("address")
        photo = request.FILES.get("photo")

        if not studentname:
            return render(request, "institute/teacher_admin/students/addstudents.html", {
                "error": "Student name required", "classroom": classroom
            })

        try:
            roll = int(roll)
            if Student.objects.filter(class_room=classroom, roll_no=roll).exists():
                raise ValueError("Roll number already exists")
        except ValueError as e:
            return render(request, "institute/teacher_admin/students/addstudents.html", {
                "error": str(e) if "exists" in str(e) else "Invalid roll number", "classroom": classroom
            })

        try:
            dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return render(request, "institute/teacher_admin/students/addstudents.html", {
                "error": "Invalid DOB", "classroom": classroom
            })

        if guardian_phone and not re.match(r'^[6-9]\d{9}$', guardian_phone):
            return render(request, "institute/teacher_admin/students/addstudents.html", {
                "error": "Enter valid 10-digit guardian phone", "classroom": classroom
            })

        Student.objects.create(
            school=school,
            class_room=classroom,
            student_name=studentname,
            roll_no=roll,
            dob=dob,
            father_name=father_name,
            guardian_phone=guardian_phone,
            address=address,
            photo=photo
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
    students = Student.objects.filter(
        class_room=teacher.classroom
    ).order_by("roll_no")

    return render(request, "institute/teacher_admin/students/viewStudents.html", {
        "students": students,
        "classroom": teacher.classroom
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
    teacher = request.teacher
    classroom = teacher.classroom
    subjects = ClassSubject.objects.filter(classroom=classroom)
    students = Student.objects.filter(class_room=classroom)

    if request.method == "POST":
        student_id = request.POST.get('student')
        exam_type = request.POST.get('exam')

        student = Student.objects.filter(id=student_id, class_room=classroom).first()

        if not student:
            return render(request, "institute/teacher_admin/marks/addMarks.html", {
                "error": "Invalid student",
                "subjects": subjects,
                "students": students
            })

        for subject in subjects:
            try:
                theory = int(request.POST.get(f'theory_{subject.id}', 0))
            except (ValueError, TypeError):
                theory = 0
            
            try:
                practical = int(request.POST.get(f'practical_{subject.id}', 0))
            except (ValueError, TypeError):
                practical = 0

            theory = max(0, min(theory, subject.theory_max))
            practical = max(0, min(practical, subject.practical_max))

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

    return render(request, "institute/teacher_admin/marks/addMarks.html", {
        "subjects": subjects,
        "students": students
    })


# ---------------- VIEW MARKS ----------------
@login_required
@teacher_required
def viewMarks(request):
    teacher = request.teacher
    exam = request.GET.get("exam", "Final")

    marks = Mark.objects.filter(
        student__class_room=teacher.classroom,
        exam=exam
    ).select_related("student", "subject")
    
    school = teacher.school

    return render(request, "institute/teacher_admin/marks/viewmarks.html", {
        "marks": marks,
        "selected_exam": exam,
        "teacher": teacher,
        "school": school,
        "classroom": teacher.classroom,
    })


# ---------------- VIEW RESULTS ----------------
@login_required
@teacher_required
def viewResults(request):
    teacher = request.teacher
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
    total_possible = sum(m.subject.theory_max + m.subject.practical_max for m in marks)

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
        'teacher': teacher,
        'school': teacher.school,
    }

    return render(request, "institute/teacher_admin/marks/viewResult.html", context)

