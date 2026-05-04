from django.urls import path
from . import views
app_name = 'billing'
urlpatterns = [
    path('', views.billing_view, name='billing'),
    path('history/', views.transaction_history, name='transaction_history'),
]
