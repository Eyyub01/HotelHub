from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelhub.settings')

app = Celery('hotelhub')

# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


CELERY_BEAT_SCHEDULE = {
    'update-expired-bookings-every-midnight': {
        'task': 'bookings.tasks.update_expired_bookings',
        'schedule': crontab(hour=0, minute=0),  # Hər gecə saat 00:00-da
    },
    'send-daily-hotel-recommendations': {
        'task': 'send_recommended_hotels_email',
        'schedule': crontab(minute=0, hour=9),  # Hər gün saat 09:00-da işləsin
    },
      'free-expired-rooms-nightly': {
        'task': 'bookings.tasks.free_expired_rooms',
        'schedule': crontab(hour=3, minute=0),  # Hər gecə saat 3:00-da
    },
}