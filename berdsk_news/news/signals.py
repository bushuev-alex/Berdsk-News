# import time
from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from datetime import datetime, timedelta

from news.models import Advertiser, News, Category


def send_notifications(pk, subject, text, name, phone, recipient_list):
    html_content = render_to_string("contact_form_submitted.html",
                                    {
                                        "name": name,
                                        "phone": phone,
                                        "subject": subject,
                                        "text": text,
                                    })

    msg = EmailMultiAlternatives(subject=subject,
                                 body="",
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=recipient_list)

    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("message sent")


@shared_task
def notify_new_form_submission(pk: int, **kwargs):
    ad = Advertiser.objects.get(id=pk)
    print(ad)
    recipient_list = [settings.DEFAULT_FROM_EMAIL]
    send_notifications(ad.pk, ad.subject, ad.text, ad.name, ad.phone, recipient_list)
    return True
