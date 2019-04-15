from django.urls import path, include


urlpatterns = [
    path('todos/', include('todo.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
]
