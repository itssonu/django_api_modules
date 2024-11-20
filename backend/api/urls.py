from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('quicstart/', include('user.urls')),
    path('snippets/', include('snippets.urls'))
]
