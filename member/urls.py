from django.urls import path
from . import views

app_name = "member"

urlpatterns = [
    path('', views.index , name='index'),
    path('edit/<int:pk>', views.edit , name='edit'),
]
