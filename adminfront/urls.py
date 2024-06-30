# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Admin_home, name='home'),


    path('admin_index.html', views.admin_index, name='admin_index'),


]
