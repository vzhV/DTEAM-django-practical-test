from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import cv_list, cv_detail, cv_pdf, CVViewSet, settings_view, send_cv_email, cv_translate

router = DefaultRouter()
router.register(r'cv', CVViewSet, basename='cv')

urlpatterns = [
    path('', cv_list, name='cv_list'),
    path('cv/<int:pk>/', cv_detail, name='cv_detail'),
    path('cv/<int:pk>/pdf/', cv_pdf, name='cv_pdf'),
    path("settings/", settings_view, name="settings"),
    path('cv/<int:pk>/send_email/', send_cv_email, name='send_cv_email'),
    path('cv/<int:pk>/translate/', cv_translate, name='cv_translate'),
    path('api/', include(router.urls)),
]
