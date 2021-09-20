"""starwars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from explorer.views import get_CSV_file_list, get_CSV_details, fetch_people_list

urlpatterns = [
    path('', get_CSV_file_list, name='get_CSV_file_list'),
    re_path(r'^detail/(?P<csv_id>\d+)$', get_CSV_details, name='get_CSV_details'),
    re_path(r'^fetch/$', fetch_people_list, name='fetch_people_list'),
    path('admin/', admin.site.urls),
]
