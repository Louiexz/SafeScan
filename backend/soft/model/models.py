import uuid

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

User = get_user_model()