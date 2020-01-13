from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import settings
from .schema import schema
from .views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="api"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
