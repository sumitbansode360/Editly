from django.shortcuts import get_object_or_404
from .models import Document
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

class DocListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'

class DocCreateView(CreateView):
    model = Document
    template_name = 'documents/document_create.html'
    fields = ['title']

    def get_success_url(self):
        return reverse_lazy('doc-edit', kwargs={'uuid': self.object.uuid})


class DocDeleteView(DeleteView):
    model = Document
    template_name = 'documents/document_delete.html'

    lookup_field = 'uuid'

    def get_object(self, queryset=None):
        """ Fetch the document using UUID instead of pk """
        return get_object_or_404(Document, uuid=self.kwargs['uuid'])  # ✅ Fetch by uuid

    success_url = reverse_lazy('doc-list')


class DocUpdateView(UpdateView):
    model = Document
    template_name = 'documents/document_update.html'
    fields = ['title', 'content']
    # Override lookup field to use UUID instead of default 'pk'
    lookup_field = 'uuid'

    def get_object(self, queryset=None):
        """ Fetch the document using UUID instead of pk """
        return get_object_or_404(Document, uuid=self.kwargs['uuid'])  # ✅ Fetch by uuid

    success_url = reverse_lazy('doc-list')
