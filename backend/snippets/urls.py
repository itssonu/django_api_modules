from django.urls import path
from .views import snippetList, storeSnippet, getSnippet, updateSnippet, deleteSnippet

urlpatterns = [
    path('', snippetList),
    path('store', storeSnippet),
    path('<int:snipetId>', getSnippet),
    path('update/<int:snipetId>', updateSnippet),
    path('delete/<int:snipetId>', deleteSnippet)
]
