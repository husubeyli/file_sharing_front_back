from __future__ import absolute_import, unicode_literals
from django.utils import timezone

from .models import File
from file_sharing.celery import app


@app.task()
def delete_file_after_seven_day(file_id):
    file = File.objects.filter(id=file_id).filter(
        is_status_expired__lte=timezone.datetime.today()).delete()



