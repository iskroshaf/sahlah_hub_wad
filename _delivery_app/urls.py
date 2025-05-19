from django.urls import path
from . import views

urlpatterns = [
    path("",            views.delivery_list_view,   name="delivery_list"),
    path("add/",        views.delivery_create_view, name="delivery_add"),
    path("<int:pk>/",   views.delivery_update_view, name="delivery_edit"),
    
]