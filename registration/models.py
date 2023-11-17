from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField


def validate_national_id(value):

    if len(value) != 10:
        raise ValidationError('National ID must be exactly 10 digits.')

    if not value.isdigit():
        raise ValidationError('National ID must contain only digits.')

    check = int(value[9])
    total = sum(int(value[i]) * (10 - i) for i in range(9)) % 11
    if (total < 2 and check == total) or (total >= 2 and check == 11 - total):
        return
    raise ValidationError('Invalid National ID checksum.')


class UserData(models.Model):
    national_id = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=r'^[0-9]*$', message='National ID must contain only digits.'),
            validate_national_id,
        ],
        unique=True,
    )
    email = models.EmailField()


class EmailStatusManager(models.Manager):
    def get_or_create_singleton(self, **kwargs):
        obj, created = self.get_or_create(**kwargs)
        return obj


class EmailStatus(models.Model):
    total_emails = models.IntegerField()
    emails_sent = models.IntegerField(default=0)
    is_sending = models.BooleanField(default=False)

    objects = EmailStatusManager()

    def save(self, *args, **kwargs):
        self.pk = 1
        super(EmailStatus, self).save(*args, **kwargs)


class EmailTemplateManager(models.Manager):
    def get_or_create_singleton(self, **kwargs):
        obj, created = self.get_or_create(**kwargs)
        return obj


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    body = RichTextField()

    objects = EmailTemplateManager()

    def save(self, *args, **kwargs):
        self.pk = 1
        super(EmailTemplate, self).save(*args, **kwargs)
