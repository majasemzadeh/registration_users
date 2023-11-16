from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_iranian_national_id(value):

    if len(value) != 10:
        raise ValidationError('National ID must be exactly 10 digits.')

    if not value.isdigit():
        raise ValidationError('National ID must contain only digits.')

    check = int(value[9])
    total = sum(int(value[i]) * (10 - i) for i in range(9)) % 11
    if (total < 2 and check == total) or (total >= 2 and check == 11 - total):
        return
    raise ValidationError('Invalid National ID checksum.')


class DataCSV(models.Model):

    csv_file = models.FileField()
    is_paused = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    national_id = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=r'^[0-9]*$', message='National ID must contain only digits.'),
            validate_iranian_national_id,
        ],
        unique=True,
    )

    email = models.EmailField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)