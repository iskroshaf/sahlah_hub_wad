from _customer_app import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', views.customer_register_view, name='customer_register'),
    path('home/', views.customer_home_view, name='customer_home'),
    path('update/',views.customer_update_profile,name="Update_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)