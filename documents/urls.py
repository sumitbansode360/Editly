from django.urls import path
from documents.views import index

urlpatterns = [
    path('dash/', index, name='index'),
]
