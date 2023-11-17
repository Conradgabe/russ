from django.urls import path
from . import views

urlpatterns = [
    path('', views.SyncCredentials.as_view(), name='sync-data')
]