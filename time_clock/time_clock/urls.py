from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_swagger.views import get_swagger_view

urlpatterns_api_user = [
    path('api/account/', include('account.urls')),
    path('api/log/', include('log.urls')),
]

urlpatterns_swagger = [
    path('api/', get_swagger_view(title='API Docs.', patterns=urlpatterns_api_user)),
]

urlpatterns = []
urlpatterns += urlpatterns_api_user

if settings.SWAGGER_SETTINGS['IS_ENABLE']:
    urlpatterns += urlpatterns_swagger

if settings.IS_HIDE_ADMIN_URL:
    urlpatterns += [
        path('hidden-admin/', admin.site.urls),
    ]
else:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
