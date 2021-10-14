
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def after_seven_day():
    return timezone.datetime.today() + timedelta(days=1)


class File(models.Model):
    # relations's
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='files')

    # informations
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='file', max_length=100)
    is_status_expired = models.DateTimeField(
        'Bitmə vaxtı', default=after_seven_day, blank=True, null=True)
    slug = models.SlugField(max_length=500, default='', editable=False)

    # moderations
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return str(self.id)


class AccessUser(models.Model):
    ACCESS_USER = (
        (0, 'NO ACCESS'),
        (1, 'SHOW'),
        (2, 'COMMIT AND SHOW'),
    )

    views_user = models.ManyToManyField(User, related_name='access_user')
    files = models.ManyToManyField(File, related_name='file_access')
    access_type = models.IntegerField(choices=ACCESS_USER, default=0)

    class Meta:
        verbose_name = 'Access user'
        verbose_name_plural = 'Access users'

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    # relation's
    users = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    files = models.ForeignKey(
        "files.File", on_delete=models.CASCADE, related_name='comments')

    # informations
    content = models.TextField()

    # moderations
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content
