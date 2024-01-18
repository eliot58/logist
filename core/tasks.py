from celery import shared_task
from .models import *
from django.conf import settings
from django.core.mail import send_mail

@shared_task(bind=True)
def call(self):
    pass