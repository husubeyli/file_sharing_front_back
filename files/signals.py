from django.db.models.signals import post_save
from django.dispatch import receiver

from .commons import slugify
from .models import File
from .tasks import delete_file_after_seven_day


@receiver(post_save, sender=File)
def create_file(sender, created, instance, **kwargs):
    if created:
        instance.slug = slugify(instance.title + "-" + str(instance.id))
        # delete_file_after_seven_day.apply_async(args=[instance.id], eta=instance.is_status_expired)
        instance.save()
