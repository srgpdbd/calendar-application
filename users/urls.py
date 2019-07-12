from django.urls import path
from users.views import Me


urlpatterns = [
    path('', Me.as_view(), name='me'),
]
