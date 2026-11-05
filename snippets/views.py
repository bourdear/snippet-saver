from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Snippet


class SnippetListView(ListView):
    model = Snippet

class SnippetDetailView(DetailView):
    model = Snippet

class SnippetCreateView(CreateView):
    model = Snippet
    fields = ['title', 'language', 'code']

class SnippetUpdateView(UpdateView):
    model = Snippet
    fields = ['title', 'language', 'code']

class SnippetDeleteView(DeleteView):
    model = Snippet
    success_url = reverse_lazy('snippets:list')
