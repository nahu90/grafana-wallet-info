from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Api V1",
      contact=openapi.Contact(email="naha90@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


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

        # Swagger
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

        # Redoc
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'backend.views.handler404'
handler500 = 'backend.views.handler500'
handler403 = 'backend.views.handler403'
