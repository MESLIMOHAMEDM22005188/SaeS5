from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from mousey import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('verify/<str:identifier>/', views.verify, name='verify'),
    path('login/', views.user_login, name='login'),
    path('logout/', include('django.contrib.auth.urls')),
    path('levelOne/', views.level_one, name='level_one'),
    path('levelOne/bureau/', views.level_one_bureau, name='level_one_bureau'),
    path('levelTwo/', views.level_two, name='level_two'),  # Correction ici
    path('levelTwoJeu1/', views.level_two_jeu1, name='level_two_jeu1'),
    path('levelThree/', views.level_three, name='level_three'),
    path('levelOne/bureau/browser', views.browser_level_one, name='browser_level_one'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('screen-warning/', views.screen_warning, name='screen_warning'),
    path('levelOneQuizz/', views.test_level1_view, name='level_one_quizz'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
