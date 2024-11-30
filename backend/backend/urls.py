from django.contrib import admin
from django.urls import include, path
from safescan.view import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    # Rota para o root (ver todas as URLs)
    path('api/', root.as_view(), name="list-urls"),  # Exibe todas as URLs do projeto
    
    # Rotas específicas para suas views
    path("api/sign-in", SignIn.as_view(), name="sign-in"),
    path("api/sign-up", SignUp.as_view(), name="sign-up"),
    path("api/forgot-password", ForgotPassword.as_view(), name="forgot-password"),
    path("api/profile/", ViewProfile.as_view(), name="profile"),
    path("api/software", ViewSoftware.as_view(), name='software'),
    path("api/software_form_unauth", SoftwareFormUnauth.as_view(), name='software_form_unauth'),
    path("api/virustotal", ViewUrlFile.as_view(), name='virustotal'),
    
    # Incluindo as URLs do app safescan (se houver outras urls neste app)
    path('', include('safescan.urls')),  # Verifique se você tem um safescan/urls.py
]