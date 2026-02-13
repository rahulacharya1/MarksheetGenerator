from django.db import models
from django.contrib.auth.models import User


class States(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Schools(models.Model):
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):

    CLASS_CHOICES = [(i, str(i)) for i in range(1, 11)]
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
    ]

    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    name = models.IntegerField(choices=CLASS_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)

    class Meta:
        unique_together = ('school', 'name', 'section')

    def __str__(self):
        return f"Class {self.name} - {self.section}"



class Students(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    studentName = models.CharField(max_length=50)
    roll_no = models.IntegerField()
    dob = models.DateField()

    def __str__(self):
        return f"{self.studentName} - {self.class_room} - Roll {self.roll_no}"
    

class Subjects(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class Marks(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    marks = models.IntegerField()
    
    class Meta:
        unique_together = ('student', 'subject')
        
