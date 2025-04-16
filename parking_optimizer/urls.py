from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('optimize/<int:config_id>/', views.optimize, name='optimize'),
    path('results/<int:config_id>/', views.results, name='results'),
    path('edit/<int:config_id>/', views.edit_config, name='edit_config'),
    path('delete/<int:config_id>/', views.delete_config, name='delete_config'),
]