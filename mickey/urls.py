from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mousey import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify/<str:method>/<str:identifier>/', views.verify, name='verify'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),  # Cette ligne redirige '/' vers la vue 'home'
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('levelOne/', views.level_one, name='level_one'),
    path('levelOne/bureau/', views.level_one_bureau, name='level_one_bureau'),
    path('levelTwo/', views.level_two, name='level_two'),
    path('levelThree/', views.level_three, name='level_three'),
]