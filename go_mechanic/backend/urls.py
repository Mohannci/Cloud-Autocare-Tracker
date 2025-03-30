from django.contrib import admin
from django.urls import path
from autocare import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('edit_vehicle/<str:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<str:vehicle_id>/', views.delete_vehicle_view, name='delete_vehicle'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('service_history/', views.service_history, name='service_history'),  # New tab
    path('appointments/', views.appointments, name='appointments'),  # New tab
    path('contact/', views.contact, name='contact'),  # New tab
    
]