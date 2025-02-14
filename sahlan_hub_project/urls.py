from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('_core_app.urls')),
    path('user/', include('_authentication_app.urls')),
    path('customer/', include('_customer_app.urls')),
    path('seller/', include('_seller_app.urls')),
    path('shop/', include('_shop_app.urls')),

    #
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),  
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
