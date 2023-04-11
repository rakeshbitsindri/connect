from django.urls import path
from .views import arista_data

urlpatterns = [
    path('arista/', arista_data, name='arista_data'),
    path('connect/', arista_data, name='arista_data'),
]
