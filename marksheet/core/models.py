from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# ---------------- STATE ----------------
class State(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------------- SCHOOL ----------------
class School(models.Model):

    BOARD_CHOICES = (
        ('CBSE', 'CBSE'),
        ('ICSE', 'ICSE'),
        ('STATE', 'State Board'),
        ('IB', 'IB'),
        ('IGCSE', 'IGCSE'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school_name = models.CharField(max_length=255)
    established_year = models.PositiveIntegerField(null=True, blank=True)

    board = models.CharField(max_length=20, choices=BOARD_CHOICES)

    affiliation_number = models.CharField(max_length=100, blank=True, null=True)

    official_email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    state = models.ForeignKey(State, on_delete=models.CASCADE)

    pincode = models.CharField(max_length=10)

    registration_certificate = models.FileField(
        upload_to='school_documents/',
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.school_name


# ---------------- ACADEMIC YEAR ----------------
class AcademicYear(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    year = models.CharField(max_length=20)  
    # example: 2025-2026

    def __str__(self):
        return f"{self.school} - {self.year}"


# ---------------- CLASSROOM ----------------
class ClassRoom(models.Model):

    CLASS_CHOICES = [(i, str(i)) for i in range(1, 13)]

    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE
    )

    name = models.IntegerField(choices=CLASS_CHOICES)

    section = models.CharField(
        max_length=1,
        choices=SECTION_CHOICES
    )

    class Meta:
        unique_together = ('school', 'academic_year', 'name', 'section')

    def __str__(self):
        return f"{self.school} - Class {self.name}{self.section} ({self.academic_year.year})"


# ---------------- TEACHER ----------------
class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    classroom = models.OneToOneField(
        ClassRoom,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.first_name} - {self.classroom}"


# ---------------- STUDENT ----------------
class Student(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    class_room = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE
    )

    student_name = models.CharField(max_length=100)

    roll_no = models.PositiveIntegerField()

    dob = models.DateField()

    class Meta:
        unique_together = ('class_room', 'roll_no')

    def __str__(self):
        return f"{self.student_name} - Roll {self.roll_no}"


# ---------------- EXAM ----------------
class Exam(models.Model):

    EXAM_TYPES = (
        ('HALF', 'Half Yearly'),
        ('FINAL', 'Final'),
    )

    name = models.CharField(max_length=50, choices=EXAM_TYPES)

    def __str__(self):
        return self.get_name_display()


# ---------------- MARK ----------------
class Mark(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    marks = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student} - {self.exam} : {self.marks}"
    
    
class ClassSubject(models.Model):

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=100)

    class Meta:
        unique_together = ('classroom', 'subject')

    def __str__(self):
        return f"{self.classroom} - {self.subject}"
    
