from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class Subject(models.Model):

    name = models.CharField(max_length=100, unique=True,blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    Profile = models.ImageField(upload_to='profile',blank=True)
    roll_no = models.IntegerField(unique=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Result(models.Model):

    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks = models.FloatField()
    total_marks = models.FloatField(null=True)

    def clean(self):
        
        if self.total_marks is None:
            raise ValidationError("Total marks cannot be null.")
        if self.marks > self.total_marks:
            raise ValidationError("Marks cannot be greater than total marks.")
    def __str__(self):
        return f"{self.student.name} - {self.marks}"
