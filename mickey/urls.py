from django.conf import settings  # Correct import
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mousey import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('verify/<str:identifier>/', views.verify, name='verify'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('levelOne/', views.level_one, name='level_one'),
    path('levelOne/bureau/', views.level_one_bureau, name='level_one_bureau'),
    path('levelTwo/', views.level_two, name='level_two'),
    path('levelThree/', views.level_three, name='level_three'),
]

# Inclure Debug Toolbar uniquement si DEBUG est activé
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
