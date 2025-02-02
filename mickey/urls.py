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
    path('levelTwo/', views.level_two, name='level_two'),
    path('levelThree/', views.level_three, name='level_three'),
    path('levelTwoJeu1/', views.level_two_jeu1, name='level_two_jeu1'),
    path('levelTwoJeu2/', views.level_two_jeu2, name='level_two_jeu2'),
    path('levelTwoJeu3/', views.level_two_jeu3, name='level_two_jeu3'),
    path('levelTwoJeu4/', views.level_two_jeu4, name='level_two_jeu4'),
    path('levelTwoPswd/', views.level_two_pswd, name='level_two_pswd'),
    path('levelThree/', views.level_three, name='level_three'),
    path('levelOne/bureau/browser', views.browser_level_one, name='browser_level_one'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('screen-warning/', views.screen_warning, name='screen_warning'),
    path('levelOneQuizz/', views.test_level1_view, name='level_one_quizz'),
    path('levelTwoQuizz/', views.test_level2_view, name='level_two_quizz'),
    path('levelThreeQuizz/', views.test_level3_view, name='level_three_quizz'),
    path('levelThreeQuizz/', views.test_level3_view, name='level_Three_quizz'),
    path('levelOneCourse/', views.level_two_course, name='level_two_course')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
