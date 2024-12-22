# myproject/urls.py

# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Built-in LoginView
    path('accounts/', include('django.contrib.auth.urls')),  # Include other auth URLs (logout, password reset)
    path('', include('qa.urls')),  # Your app URLs
]
