from django.urls import path
from . import views

urlpatterns = [
    path('', views.private_page, name='private_page'),
    path('verify/', views.public_verification_page, name='public_verification_page'),
    path('api/register/', views.register, name='register'),
    path('api/sign/', views.sign, name='sign'),
    path('api/verify_signature/', views.verify, name='verify_signature'),
]
