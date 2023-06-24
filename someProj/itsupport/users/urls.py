from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
 path('', views.index, name='home'),
 path('register/',views.register,name='register'),
 path('login/', views.login_view, name='login'),
 path('problem/',views.create_problem,name='problem'),
 path('problems/',views.problem_list,name='problems'),
 path('problems/<str:problem_type>/', views.problem_list, name='problem_list_filtered'),
 path('problem/<int:problem_id>/', login_required(views.problem_detail), name='problem_detail'),
 path('problem/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
  path('problems/<int:problem_id>/solve/', views.solve_problem, name='solve_problem'),
]