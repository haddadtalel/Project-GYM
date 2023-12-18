from django.urls import path
from . import views

app_name = "coach"

urlpatterns = [
    path('', views.index , name='index'),
    path('edit/<int:pk>', views.edit , name='edit'),
    path('attendance/<int:pk>/<int:id>', views.attendance , name='attendance'),
    path('activity/', views.activity , name='activity'),
    path('book/', views.book , name='book'),
    path('active/<int:pk>', views.active , name='active'),
    path('deactivate/<int:pk>', views.deactivate , name='deactivate'),
    path('delete/<int:pk>', views.delete , name='delete'),
]
