from django.urls import path
from . import views  # Adjust based on your views file

urlpatterns = [
    path('', views.home, name='autocare_home'),  # Example, adjust as needed
    # Add other URL patterns for autocare views
]