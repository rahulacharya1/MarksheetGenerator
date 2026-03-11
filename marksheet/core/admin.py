from django.contrib import admin
from .models import *


# ---------------- STATE ----------------
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ---------------- SCHOOL ----------------
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "school_name",
        "board",
        "official_email",
        "phone",
        "state",
        "is_verified",
    )

    list_filter = ("state", "board", "is_verified")

    search_fields = (
        "school_name",
        "official_email",
        "phone",
    )


# ---------------- ACADEMIC YEAR ----------------
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("school", "year")
    list_filter = ("school",)


# ---------------- CLASSROOM ----------------
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = (
        "school",
        "academic_year",
        "name",
        "section",
    )

    list_filter = (
        "school",
        "academic_year",
    )


# ---------------- TEACHER ----------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "school",
        "classroom",
    )

    list_filter = ("school",)


# ---------------- STUDENT ----------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "roll_no",
        "class_room",
        "school",
    )

    list_filter = (
        "school",
        "class_room",
    )

    search_fields = (
        "student_name",
        "roll_no",
    )


# ---------------- EXAM ----------------
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name",)


# ---------------- MARK ----------------
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "exam",
        "marks",
    )

    list_filter = (
        "exam",
    )

    search_fields = (
        "student__student_name",
    )
    
    
# ---------------- CLASSSUBJECT ----------------
@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):

    list_display = (
        "classroom",
        "subject",
    )

    list_filter = (
        "classroom",
    )
    
