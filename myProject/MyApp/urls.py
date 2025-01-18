from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('home/', views.home, name='home'),
    path('', include('authentication.urls')),
    path('', include('userprofile.urls')),
    path('admin/', admin.site.urls),
]
