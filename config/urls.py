from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions, response, reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


# Authentication-related URLs
auth_urls = [
    path("", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# App-specific URLs
urls = [
    path("", include("cart.urls")),
    path("", include("customers.urls")),
    path("", include("orders.urls")),
    path("", include("payments.urls")),
    path("", include("catalogue.urls")),
    path("", include("stores.urls")),
    path("", include("wishlist.urls")),
]

# Swagger, ReDoc, and Schema URLs
swagger_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Main URL patterns
urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),  # Debug Toolbar
    path("admin/", admin.site.urls),  # Admin
    path("auth/", include(auth_urls)),  # Authentication
    path("api/v1/", include(urls)),  # API v1 namespace
] + swagger_urls  # Include Swagger and ReDoc URLs

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

class APIRoot(APIView):
    """
    Root API view that lists all major resource endpoints.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        return response.Response({
            "products": reverse.reverse("products", request=request, format=format),
            "stores": reverse.reverse("store-list", request=request, format=format),
            "cart": reverse.reverse("cart", request=request, format=format),
            "orders": reverse.reverse("orders", request=request, format=format),
        })


urlpatterns.append(path("", APIRoot.as_view()))  # Add API root
