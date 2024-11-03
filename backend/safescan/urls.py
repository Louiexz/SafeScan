from django.urls import path

from safescan.view import *

urlpatterns = [
    path("sign-in", sign_in, name="sign-in"),
    path("sign-up", sign_up, name="sign-up"),
    path("retrieve-password", retrieve_password, name="retrieve-password"),
    path("profile/", view_profile, name="profile"),
    path("", view_software, name='software'),
]
