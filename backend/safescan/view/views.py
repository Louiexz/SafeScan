from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..model import Software, User
from ..serializer import SoftwareSerializer, UserSerializer
from rest_framework import status

@api_view(['GET', 'POST'])
def view_home(request):
    if request.method == 'POST':
        return redirect("todo")
    
    return Response({'message': 'api on'})

