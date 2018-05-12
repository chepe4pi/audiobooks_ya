from django.conf import settings
from django.db import models

from abook_generating.tasks import generate_abook


class ABookGeneration(models.Model):
    ABOOK_STATUS_CHOICES = (
        ('init', 'Preparing data'),
        ('generating', 'Generating ABook'),
        ('error', 'Generation failed'),
        ('done', 'Generation completed')
    )

    LANGS_CHOICES = (
        ("ru-RU", "ru-RU"),
        ("en-EN", "en-EN"),
        ("tr-TR", "tr-TR"),
        ("uk-UA", "uk-UA")
    )

    GENDER_CHOICES = (
        ('unknown', 'unknown'),
        ('male', 'male'),
        ('female', 'female')
    )

    book_text = models.FileField()
    book_name = models.CharField(max_length=127)
    status = models.CharField(choices=ABOOK_STATUS_CHOICES, max_length=20, default='init')
    generated_file = models.FilePathField()
    lang = models.CharField(choices=LANGS_CHOICES, max_length=10, default="ru-RU")
    speaker = models.CharField(max_length=50, default=settings.DEFAULT_SPEAKER)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default='unknown')
    error_log = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.book_name, self.status)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        generate_abook(self.pk)
