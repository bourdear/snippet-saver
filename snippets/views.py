from django.views.generic import CreateView, DetailView, ListView
from .models import Snippet


class SnippetListView(ListView):
    model = Snippet

class SnippetDetailView(DetailView):
    model = Snippet

class SnippetCreateView(CreateView):
    model = Snippet
    fields = ['title', 'language', 'code']
