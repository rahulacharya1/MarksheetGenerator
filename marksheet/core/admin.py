from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(State)
admin.site.register(School)
admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Mark)

