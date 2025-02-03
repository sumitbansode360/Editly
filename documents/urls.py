from django.urls import path
from documents.views import DocListView, DocCreateView, DocDeleteView, DocUpdateView

urlpatterns = [
    path('list/', DocListView.as_view(), name='doc-list'),
    path('create/', DocCreateView.as_view(), name='doc-create'),
    path('edit/<str:uuid>/', DocUpdateView.as_view(), name='doc-edit'),
    path('delete/<str:uuid>/', DocDeleteView.as_view(), name='doc-delete'),
]
