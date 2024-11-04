from django.urls import path

from safescan.view import *

urlpatterns = [
    path("sign-in", sign_in, name="sign-in"),
    path("sign-up", sign_up, name="sign-up"),
    path("forgot-password", forgot_password, name="forgot-password"),
    path("reset-password/<str:uidb64>/<str:token>/", reset_password_confirm, name="reset-password"),
    path("profile/", view_profile, name="profile"),
    path("", view_software, name='software'),
    path("delete-software/<uuid:id>/", delete_software, name='delete-software'),
]
