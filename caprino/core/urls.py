from django.urls import path
from . import views

app_name = 'caprino.core'
urlpatterns = [
    path('', views.home, name='home'),
]
