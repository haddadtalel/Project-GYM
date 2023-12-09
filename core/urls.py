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

    path('user/', include("user.urls",namespace="user")),
    path('schedule/', include("schedule.urls",namespace="schedule")),
    path('equipment/', include("equipment.urls",namespace="equipment")),
    path('package/', include("package.urls",namespace="package")),
    path('member/', decorator_include(login_required,"member.urls",namespace="member")),
    path('coach/', include("coach.urls",namespace="coach")),
    path('transaction/', include("transaction.urls",namespace="transaction")),
]
