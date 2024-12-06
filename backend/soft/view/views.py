from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from ..model import Software, User
from ..serializer import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.urls import get_resolver
from rest_framework.response import Response

class root(APIView):
    def get(self, request):
        # Obtém o resolver de URLs atual
        resolver = get_resolver()

        # Lista para armazenar todas as URLs
        url_list = []

        # Itera sobre todos os padrões de URL
        for pattern in resolver.url_patterns:
            # Verifica se o padrão de URL possui um nome e um padrão de URL
            if hasattr(pattern, 'name') and pattern.name:
                # A URL pode ter parâmetros como `<int:id>`, então pegamos o padrão real
                url_pattern = str(pattern.pattern)
                url_list.append(f'{pattern.name}: {url_pattern}')

        return Response({
            'message': 'List of all available URLs:',
            'urls': url_list
        })