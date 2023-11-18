import logging
import threading
from time import sleep

from django.core.validators import EmailValidator
from django.template import Context, Template
from rest_framework.exceptions import ValidationError

from registration.models import UserData, validate_national_id, EmailStatus, UserDataStatus
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction


def validate_email(value):
    email_validator = EmailValidator(message='Enter a valid email address.')
    try:
        email_validator(value)
    except ValidationError as e:
        # Validation failed, handle the error as needed
        raise ValidationError('Invalid email format.') from e


# Checking rows & Insert in table


pause_event = threading.Event()


def send_email_background(email_status):

    for user_data in UserData.objects.all():
        if pause_event.is_set():
            break  # Pause the process sending email

        sleep(2) # like getting 2second for send an email

        email_status.refresh_from_db()

        email_status.emails_sent += 1
        email_status.save(update_fields=["emails_sent"])

    email_status.is_sending = False
    email_status.save()


# This function use for dynamic email template
def render_template(template_text, context_data):

    template = Template(template_text)
    context = Context(context_data)
    rendered_text = template.render(context)

    return rendered_text


def process_row(row):
    logger = logging.getLogger(__name__)

    try:
        logger.warning(row)
        national_id, email = row
        validate_email(email)
        validate_national_id(national_id)
        UserData.objects.create(national_id=national_id, email=email)
    except Exception as e:
        return f"Error processing row {row}: {str(e)}"


def insert_data(rows: list):
    logger = logging.getLogger(__name__)
    logger.warning("run")
    rows_list = list(rows)

    # Check the length
    rows_length = len(rows_list)

    logger.warning(rows_length)

    data_status = UserDataStatus.objects.create()

    email_status = EmailStatus.objects.all().first()
    email_status.total_emails = rows_length
    email_status.save()
    with transaction.atomic():
        with ThreadPoolExecutor() as executor:
            errors = list(executor.map(process_row, rows))

        error_messages = [error for error in errors if error]

        data_status.errors=str(error_messages)
        data_status.inserted=True
        data_status.save()

        email_status = EmailStatus.objects.all().first()
        email_status.total_emails = rows_length-len(errors)
        email_status.save()