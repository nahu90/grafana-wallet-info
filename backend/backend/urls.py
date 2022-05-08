from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Django ADMIN
    re_path(r'^admin/', admin.site.urls),

    # Core
    #re_path(r'api/v1/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        # Rosseta - Translations
        re_path(r'^rosetta/', include('rosetta.urls')),
    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'backend.views.handler404'
handler500 = 'backend.views.handler500'
handler403 = 'backend.views.handler403'
