# queryapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.query_view, name='query_view'),  # This should match the URL you're trying to access
]
