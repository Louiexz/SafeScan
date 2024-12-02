from django.test import TestCase
from django.urls import reverse
from ..model import User, Software
from django.contrib.auth.hashers import make_password, check_password