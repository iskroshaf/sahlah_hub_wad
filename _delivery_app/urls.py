from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='nama_app_home'),
    # path('detail/<int:pk>/', views.detail, name='nama_app_detail'),
]