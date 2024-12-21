from django.urls import path
from . import views

app_name = 'tutor'  # Ensure the app has a namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors/<int:mentor_id>/', views.mentor_profile, name='mentor_profile'),  # Add this line
]
