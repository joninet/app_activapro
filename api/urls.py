from django.urls import path, include
from .views.auth import RegisterView, CoachActivationWebhookView

urlpatterns = [
    path('auth/', include('api.urls.auth')),
]