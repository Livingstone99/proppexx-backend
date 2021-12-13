from django.contrib import admin
from rest_framework import permissions
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# swagger imports
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Propexx API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('social-auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
    path('account/', include('users.urls')),
    path('feedback/', include('feedback.urls')),
    path('rating/', include('rating.urls')),
    path('article/', include('article.urls')),
    path('verification/', include('verification.urls')),
    path('subscription/', include('subscription.urls')),
    path('property/', include('property.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('documents/', include('documents.urls')),
    path('property-request-review/', include('review.urls')),
    path('team-member/', include('team.urls')),
    path('property-request/', include('property_request.urls')),
    path('otp/', include('otp.urls')),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
