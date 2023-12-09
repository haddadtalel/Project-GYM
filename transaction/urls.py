from django.urls import path
from . import views

app_name = "transaction"

urlpatterns = [
    path('', views.index , name='index'),
]
