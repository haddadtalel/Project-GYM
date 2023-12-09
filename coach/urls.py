from django.urls import path
from . import views

app_name = "coach"

urlpatterns = [
    path('', views.index , name='index'),
    path('edit/<int:pk>', views.edit , name='edit'),
    path('book/', views.book , name='book'),
]
