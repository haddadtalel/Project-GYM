from django.contrib import admin
from django.urls import path, include
from . import views
from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='login'),
    path('logout/', views.logout, name='logout'),

    path('managerDashboard/', views.managerDashboard, name='managerDashboard'),
    path('employeeDashboard/', views.employeeDashboard, name='employeeDashboard'),
    path('coachDashboard/', views.coachDashboard, name='coachDashboard'),

    path('user/', decorator_include(login_required,"user.urls",namespace="user")),
    path('schedule/', decorator_include(login_required,"schedule.urls",namespace="schedule")),
    path('equipment/', decorator_include(login_required,"equipment.urls",namespace="equipment")),
    path('package/', decorator_include(login_required,"package.urls",namespace="package")),
    path('member/', decorator_include(login_required,"member.urls",namespace="member")),
    path('coach/', decorator_include(login_required,"coach.urls",namespace="coach")),
    path('transaction/', decorator_include(login_required,"transaction.urls",namespace="transaction")),
]
