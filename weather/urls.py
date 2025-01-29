from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Map the root URL to the index view
]