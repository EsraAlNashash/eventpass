from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(url='/scan/'), name='home'),
    path('health/', views.health_check, name='health_check'),
    path('scan/', views.scan_page, name='scan'),
    path('api/checkin/', views.checkin_api, name='checkin_api'),
]
