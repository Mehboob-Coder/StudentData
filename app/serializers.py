from rest_framework import serializers
from .models import Subject, Student,Result
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    subject = serializers.CharField() 

    class Meta:
        model = Student
        fields = ['id', 'user', 'subject', 'name', 'Profile', 'roll_no', 'address']


    def create(self, validated_data):
        subject_name = validated_data.pop('subject')
        user = self.context['request'].user

        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            raise ValidationError({"subject": f"Subject with the name '{subject_name}' does not exist."})

        return Student.objects.create(user=user, subject=subject, **validated_data)
    

class ResultSerializer(serializers.ModelSerializer):
    student = serializers.CharField(write_only=True) 
    subject = serializers.CharField(write_only=True)  
    student_name = serializers.CharField(source='student.name', read_only=True) 
    subject_name = serializers.CharField(source='subject.name', read_only=True)  
    percentage = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True)


    class Meta:
        model = Result
        fields = ['id', 'student', 'subject', 'student_name', 'subject_name', 'total_marks', 'marks', 'percentage', 'status']
    def validate(self, data):
        marks = data.get('marks')
        total_marks = data.get('total_marks')

        if marks is not None and total_marks is not None:
            if marks > total_marks:
                raise serializers.ValidationError({"marks": "Marks cannot exceed total marks."})

        return data
    
    def create(self, validated_data):
        student_name = validated_data.pop('student')
        subject_name = validated_data.pop('subject')
        student, _ = Student.objects.get_or_create(name=student_name)
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        validated_data['student'] = student
        validated_data['subject'] = subject
        return Result.objects.create(**validated_data)




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email','password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')          
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],

        )
        user.set_password(password)  
        user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            'username': user.username,
            'email': user.email,
            'token': token.key,
            "message": "User registered successfully."
        }
   
