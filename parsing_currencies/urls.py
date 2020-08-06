from django.urls import path
from . import views

urlpatterns = [
    path('currencies/', views.currencies, name='currencies'),
    path('test/', views.get_currencies),
]
