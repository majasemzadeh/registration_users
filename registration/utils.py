import threading
from time import sleep

from django.core.validators import EmailValidator
from django.template import Context, Template
from rest_framework.exceptions import ValidationError
from registration.models import UserData, validate_national_id


def validate_email(value):
    email_validator = EmailValidator(message='Enter a valid email address.')
    try:
        email_validator(value)
    except ValidationError as e:
        # Validation failed, handle the error as needed
        raise ValidationError('Invalid email format.') from e


# Checking rows & Insert in table
def process_row(row):
    try:
        national_id, email = row
        validate_email(email)
        validate_national_id(national_id)
        UserData.objects.create(national_id=national_id, email=email)
    except Exception as e:
        return f"Error processing row {row}: {str(e)}"


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
