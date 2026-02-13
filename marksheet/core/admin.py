from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(States)
admin.site.register(Schools)
admin.site.register(ClassRoom)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Marks)

