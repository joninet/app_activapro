# api/urls/auth/urls.py

from django.urls import path
from ...views.auth import RegisterView, CoachActivationWebhookView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('payment/coach-activate/', CoachActivationWebhookView.as_view(), name='coach_activation_webhook'),
]