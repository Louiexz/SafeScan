from django.contrib import admin
from django.urls import include, path
from safescan.view import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota para o root (ver todas as URLs)
    path('api/', root.as_view(), name="list-urls"),  # Exibe todas as URLs do projeto
    
    # Rotas específicas para suas views
    path("api/sign-in", sign_in.as_view(), name="sign-in"),
    path("api/sign-up", sign_up.as_view(), name="sign-up"),
    path("api/forgot-password", forgot_password.as_view(), name="forgot-password"),
    path("api/profile/", view_profile.as_view(), name="profile"),
    path("api/software", view_software.as_view(), name='software'),
    path("api/software_form_unauth", software_form_unauth.as_view(), name='software_form_unauth'),
    path("api/virustotal", view_url_file.as_view(), name='virustotal'),
    path("", index, name="frontend"),
    
    # Incluindo as URLs do app safescan (se houver outras urls neste app)
    path('', include('safescan.urls')),  # Verifique se você tem um safescan/urls.py
]