from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class School(models.Model):

    BOARD_CHOICES = (
        ('CBSE', 'CBSE'),
        ('ICSE', 'ICSE'),
        ('STATE', 'State Board'),
        ('IB', 'IB'),
        ('IGCSE', 'IGCSE'),
    )

    # One School = One Account
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic Info
    school_name = models.CharField(max_length=255)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    board = models.CharField(max_length=20, choices=BOARD_CHOICES)
    affiliation_number = models.CharField(max_length=100, blank=True, null=True)

    # Contact
    official_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    # Address
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10)

    # Verification
    registration_certificate = models.FileField(
        upload_to='school_documents/',
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.school_name


class ClassRoom(models.Model):

    CLASS_CHOICES = [(i, str(i)) for i in range(1, 13)]
    SECTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.IntegerField(choices=CLASS_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)

    class Meta:
        unique_together = ('school', 'name', 'section')

    def __str__(self):
        return f"{self.school} - Class {self.name} {self.section}"


class Student(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    roll_no = models.PositiveIntegerField()
    dob = models.DateField()

    class Meta:
        unique_together = ('class_room', 'roll_no')

    def __str__(self):
        return f"{self.student_name} - Roll {self.roll_no}"


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Mark(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject} : {self.marks}"

