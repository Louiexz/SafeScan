from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from ..model import Software, User
from ..serializer import UserSerializer, RegisterSerializer
from ..serializer import SoftwareSerializer, GetSoftwareSerializer, ProfileSoftwareSerializer
from rest_framework import status