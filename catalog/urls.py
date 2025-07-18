#use include() to add paths from the catalog application
from django.urls import include
from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
] 
