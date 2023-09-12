"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('status', views.status),
    path('aircrafts/', views.aircraft_list),
    path('aircrafts/jobs/available', views.available_aircraft),
    path('aircraft/<str:model_id>/', views.get_aircraft),
    path('airports/', views.airport_list),
    path('airport/<str:icao>', views.get_airport),
    path('assignments/<str:icao>', views.get_assignments_by_airport),
    re_path(r'^jobs/(?P<icao>\w{3,4})\/$', views.get_jobs),
    re_path(r'^jobs/(?P<aircraft>\w{5,})\/$', views.get_jobs_by_aircraft)
]
