from django.urls import path, include
# from rest_framework import urls

urlpatterns = [
    path('', include('rest_framework.urls'))
]
