from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view using OpenAPI 3.x
schema_view = get_schema_view(
    openapi.Info(
        title="Soft.ai API",
        default_version='v1',  # You can specify your version here, such as 'v1'
        description="API documentation for the Soft.ai",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

