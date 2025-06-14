from django.urls import path
from .views import recent_requests

urlpatterns = [
    path("logs/", recent_requests, name="recent_requests"),
]
