from rest_framework import viewsets,status,filters
from .models import Student, Subject,Result
from .serializers import StudentSerializer, SubjectSerializer, UserSerializer ,ResultSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.db.models import F, ExpressionWrapper,IntegerField,OuterRef, FloatField, Case, When, Value,CharField,Subquery
from django.db.models import Sum,Window
from django.db.models.functions import Coalesce
from rest_framework.decorators import action



class Signup(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors)
    

class Login(viewsets.ViewSet):
    """This class handle login functionality
    login with username and password or email and password"""
    permission_classes = [AllowAny]

    def create(self, request):
        username_or_email = request.data.get("username")
        password = request.data.get("password")

        user_query = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
        user = None
        if user_query:
            user = authenticate(username=user_query.username, password=password)
               
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response(
                    {
                        "token": token.key,
                        "message": "Login successful.",
                        
                        "user_data":serializer.data,
                        
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class Logout(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def create(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."})


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        queryset = self.queryset.annotate(
            percentage = (F('marks') * 100.0 / F('total_marks')), 
            status=Case(
                When(marks__gte = F('total_marks') / 2, then=Value("Pass")),
                default = Value("Fail"),
                output_field = CharField()
            )
        )
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        MarksStudent = queryset.aggregate(Sum('marks'))
       
        return Response({
            "results": serializer.data, 
            "MarksStudent": MarksStudent or 0,

        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            result = Result.objects.annotate(
                percentage = (F('marks') * 100.0 / F('total_marks')),
                status=Case(
                    When(marks__gte=F('total_marks') / 2, then=Value("Pass")),
                    default=Value("Fail"),
                    output_field = CharField()
                )
            ).get(pk = result.pk)

            return Response(self.get_serializer(result).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






  