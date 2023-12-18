from django.urls import path
from . import views

app_name = "member"

urlpatterns = [
    path('', views.index , name='index'),
    path('admin_view/', views.adminView , name='admin_view'),
    path('edit/<int:pk>', views.edit , name='edit'),
    path('payment_history/<int:pk>/<str:month>/<int:year>', views.paymentHistory , name='payment_history'),
    path('bill/', views.bill , name='bill'),
    path('pay/', views.pay , name='pay'),
    path('active/<int:pk>', views.active , name='active'),
    path('deactivate/<int:pk>', views.deactivate , name='deactivate'),
    path('delete/<int:pk>', views.delete , name='delete'),
]
