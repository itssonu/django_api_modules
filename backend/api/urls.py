from django.urls import path, include

urlpatterns = [
    path('quicstart/', include('user.urls')),
    path('snippets/', include('snippets.urls')),
    path('user/', include('user.urls'))
]
