from django.contrib import admin
from .models import Student , Subject, Result
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','user','subject','name','Profile','roll_no','address']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id','student','subject','marks',"total_marks"]