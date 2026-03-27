from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# ---------------- STATE ----------------
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------------- SCHOOL ----------------
class School(models.Model):

    BOARD_CHOICES = (
        ('CBSE','CBSE'),
        ('ICSE','ICSE'),
        ('STATE','State Board'),
        ('IB','IB'),
        ('IGCSE','IGCSE')
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
        upload_to='school_documents/', null=True, blank=True,
        storage=RawMediaCloudinaryStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    logo = models.ImageField(
        upload_to='school_logos/', null=True, blank=True
    )
    
    principal_sign = models.ImageField(upload_to='principal_signs/', blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.school_name


# ---------------- ACADEMIC YEAR ----------------
class AcademicYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year = models.CharField(max_length=20)

    class Meta:
        unique_together = ('school', 'year')

    def __str__(self):
        return f"{self.school} - {self.year}"


# ---------------- CLASSROOM ----------------
class ClassRoom(models.Model):

    CLASS_CHOICES = [(i, str(i)) for i in range(1, 13)]
    SECTION_CHOICES = (('A','A'),('B','B'),('C','C'))

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    name = models.IntegerField(choices=CLASS_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)

    class Meta:
        unique_together = ('school','academic_year','name','section')

    def __str__(self):
        return f"{self.school} - Class {self.name}{self.section} ({self.academic_year.year})"


# ---------------- TEACHER ----------------
class Teacher(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    teacher_sign = models.ImageField(upload_to='teacher_signs/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.classroom}"


# ---------------- CLASS SUBJECT ----------------
class ClassSubject(models.Model):

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    full_marks = models.IntegerField(default=100)
    theory_max = models.IntegerField(default=70)
    practical_max = models.IntegerField(default=30)

    class Meta:
        unique_together = ('classroom','subject')

    def __str__(self):
        return f"{self.classroom} - {self.subject}"


# ---------------- STUDENT ----------------
class Student(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    roll_no = models.PositiveIntegerField()
    dob = models.DateField()
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        unique_together = ('class_room','roll_no')

    def __str__(self):
        return f"{self.student_name} - Roll {self.roll_no}"


# ---------------- MARK ----------------
class Mark(models.Model):

    EXAM_CHOICES = (
        ('Half Yearly','Half Yearly'),
        ('Final','Final')
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    exam = models.CharField(max_length=50, choices=EXAM_CHOICES)

    theory_marks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    practical_marks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('student','subject','exam')

    def clean(self):
        if self.theory_marks > self.subject.theory_max:
            raise ValidationError("Theory marks exceed maximum limit")

        if self.practical_marks > self.subject.practical_max:
            raise ValidationError("Practical marks exceed maximum limit")

    def total_marks(self):
        return self.theory_marks + self.practical_marks

    def __str__(self):
        return f"{self.student} - {self.subject.subject} - {self.exam} : {self.total_marks()}"
    
