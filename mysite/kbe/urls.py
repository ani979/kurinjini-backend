from django.urls import path

from . import views

urlpatterns = [
    path('api/customers/', views.CustomerListCreate.as_view())
]