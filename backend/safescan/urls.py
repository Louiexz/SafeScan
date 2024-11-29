from .view import *  # Certifique-se de que 'list_urls' esteja importado aqui
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/profile-update/', UpdateProfile.as_view(), name='profile-update'),
    path("api/reset-password/<str:uidb64>/<str:token>/", ResetPasswordConfirm.as_view(), name="reset-password"),
    path("api/delete-software/<uuid:id>/", DeleteSoftware.as_view(), name='delete-software'),
    path("api/software_form_auth", SoftwareFormAuth.as_view(), name='software_form_auth'),
    path("api/sign-out", SignOut.as_view(), name="sign-out"),
]
