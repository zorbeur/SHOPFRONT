from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Administration Django Standard
    path('django-admin/', admin.site.urls),

    # Backoffice Admin E-SHOP (Sneat Theme)
    path('adminfront/', include('adminfront.urls')),
    path('super/', include('adminfront.urls')),

    # Boutique Storefront
    path('', include('frontend.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static('/categorie/', document_root=settings.CATEGORIE_ROOT)

# Handlers d'erreurs HTTP personnalisés
handler404 = 'frontend.views.custom_page_not_found_view'
handler500 = 'frontend.views.custom_server_error_view'
handler403 = 'frontend.views.custom_permission_denied_view'
handler400 = 'frontend.views.custom_bad_request_view'
