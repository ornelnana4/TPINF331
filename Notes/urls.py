from django.urls import path
from Notes import views

urlpatterns = [
    path('choose_account', views.choose_account, name='choose_account'),
    path('student', views.register_student, name='student'),
    path('choice_eu/<str:matricule>/', views.choisir_ue, name='choice_ue'),
    path('choisir', views.choisir_ue2, name='choisir'),
    path('teacher', views.register_teacher, name='teacher'),
    path('login_student', views.login_student, name='login_student'),
    path('login_teacher', views.login_teacher, name='login_teacher'),
    path('mainstudent', views.mainstudent, name='mainstudent'),

]