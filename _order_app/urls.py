from django.urls import path
from . import views


app_name = 'order'          # <─ inilah namespace

urlpatterns = [
    path('<int:order_id>/', views.order_detail, name='detail'),
]