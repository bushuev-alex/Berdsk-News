import os
from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'berdsk_news.settings')

app = Celery('berdsk_news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.enable_utc = False
app.conf.timezone = "Asia/Novosibirsk"

# app.conf.beat_schedule = {'action_every_monday_8am': {'task': 'news.signals.notify_about_posts_mon_8am',
#                                                       'schedule': crontab(hour=8, minute=0, day_of_week=1),
#                                                       }
#                           }
