from django.urls import path
from . import views
app_name = 'contacts'
urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('import/', views.import_contacts, name='import_contacts'),
]
