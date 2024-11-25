from .view import *  # Certifique-se de que 'list_urls' esteja importado aqui
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/profile-update/', update_profile.as_view(), name='profile_update'),
    path("api/reset-password/<str:uidb64>/<str:token>/", reset_password_confirm.as_view(), name="reset-password"),
    path("api/delete-software/<uuid:id>/", delete_software.as_view(), name='delete-software'),
    path("api/software_form_auth", software_form_auth.as_view(), name='software_form_auth'),
    path("api/sign-out", sign_out.as_view(), name="sign-out"),
]
