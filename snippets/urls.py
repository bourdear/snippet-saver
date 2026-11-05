from django.urls import path
from . import views

app_name = 'snippets'

urlpatterns = [
    path('', views.SnippetListView.as_view(), name='list'),
    path('new/', views.SnippetCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SnippetDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.SnippetUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SnippetDeleteView.as_view(), name='delete'),
]