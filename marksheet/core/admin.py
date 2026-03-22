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
        "created_at",
    )

    list_filter = ("state", "board", "is_verified")

    search_fields = (
        "school_name",
        "official_email",
        "phone",
    )

    readonly_fields = ("created_at",)


# ---------------- ACADEMIC YEAR ----------------
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("school", "year")
    list_filter = ("school",)
    search_fields = ("year",)


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
        "name",
    )

    search_fields = ("section",)


# ---------------- TEACHER ----------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "school",
        "classroom",
    )

    list_filter = ("school",)
    search_fields = ("user__username",)


# ---------------- CLASS SUBJECT ----------------
@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):

    list_display = (
        "classroom",
        "subject",
        "theory_max",
        "practical_max",
    )

    list_filter = (
        "classroom",
    )

    search_fields = ("subject",)


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


# ---------------- MARK ----------------
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "exam",
        "theory_marks",
        "practical_marks",
        "total_marks_display",
    )

    list_filter = (
        "exam",
        "subject",
    )

    search_fields = (
        "student__student_name",
        "subject__subject",
    )

    def total_marks_display(self, obj):
        return obj.total_marks()
    total_marks_display.short_description = "Total Marks"
    
