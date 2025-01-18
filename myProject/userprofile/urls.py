from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('timetable/', views.profile_view, name='timetable'),
      
  
]
