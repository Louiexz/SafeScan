from .view import *  # Certifique-se de que 'list_urls' esteja importado aqui
from django.urls import path

urlpatterns = [
    path("api/reset-password/<str:uidb64>/<str:token>/", reset_password_confirm.as_view(), name="reset-password"),
    path("api/delete-software/<uuid:id>/", delete_software.as_view(), name='delete-software'),
    path("api/sign-out", sign_out.as_view(), name="sign-out"),
]
