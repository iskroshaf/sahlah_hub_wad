from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
# import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('_core_app.urls')),
    path('user/', include('_user_app.urls')),
    path('customer/', include('_customer_app.urls')),
    path('seller/', include('_seller_app.urls')),
    path('shops/', include('_shop_app.urls')),

    path('set-language/', set_language, name='set_language'),
    path("__reload__/", include("django_browser_reload.urls")),

]

if settings.DEBUG:
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),  
    # ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
