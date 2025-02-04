from django.shortcuts import get_object_or_404
from .models import Document
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DocumentForm

class DocListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'documents/document_list.html'
    login_url = 'login'


class DocCreateView(LoginRequiredMixin, CreateView):
    model = Document
    template_name = 'documents/document_create.html'
    login_url = 'login'    
    fields = ['title']

    def get_success_url(self):
        return reverse_lazy('doc-edit', kwargs={'uuid': self.object.uuid})


class DocDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'documents/document_delete.html'
    login_url = 'login'


    lookup_field = 'uuid'

    def get_object(self, queryset=None):
        """ Fetch the document using UUID instead of pk """
        return get_object_or_404(Document, uuid=self.kwargs['uuid'])  # ✅ Fetch by uuid

    success_url = reverse_lazy('doc-list')


class DocUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'documents/document_update.html'
    login_url = 'login'
    form_class = DocumentForm  #use a ck editor form

    # Override lookup field to use UUID instead of default 'pk'
    lookup_field = 'uuid'

    def get_object(self, queryset=None):
        """ Fetch the document using UUID instead of pk """
        return get_object_or_404(Document, uuid=self.kwargs['uuid'])  # ✅ Fetch by uuid

    success_url = reverse_lazy('doc-list')
