import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(pk=user_id)
    print(user)
    expiration = now() + timedelta(hours=48)
    print(expiration)
    record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
    print(record)
    record.send_verification_email()
