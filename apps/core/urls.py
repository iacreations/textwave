from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('quick-send/', views.quick_send, name='quick_send'),
]
