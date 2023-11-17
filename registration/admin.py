from django.contrib import admin

from registration.models import UserData, EmailStatus, EmailTemplate

# Register your models here.
admin.site.register(UserData)
admin.site.register(EmailStatus)
admin.site.register(EmailTemplate)