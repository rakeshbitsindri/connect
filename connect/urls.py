from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_device/', views.add_device, name='add_device'),
    path('delete_device/<int:device_id>/', views.delete_device, name='delete_device'),
    path('edit_device/<int:device_id>/', views.edit_device, name='edit_device'),
    path('arista_data/', views.arista_data, name='arista_data'),
    path('generic_command/<str:cmd>/', views.generic_command, name='generic_command'),
]
