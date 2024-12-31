from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from app.views import StudentViewSet, SubjectViewSet,Signup,Login,Logout,ResultViewSet
from rest_framework.authtoken.views import ObtainAuthToken

router = DefaultRouter()
router.register('signup',Signup,basename='signup')
router.register('login',Login,basename='login')
router.register('logout',Logout,basename='logout')
router.register('students', StudentViewSet, basename='student')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('results', ResultViewSet, basename='results')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('gettoken/', ObtainAuthToken.as_view()),
]
