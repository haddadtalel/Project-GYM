from django.urls import path
from . import views

app_name = "transaction"

urlpatterns = [
    path('', views.index , name='index'),
    path('payE/<int:pk>', views.payE , name='payE'),
    path('payC/<int:pk>', views.payC , name='payC'),
]
