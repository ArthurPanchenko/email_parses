from django.contrib import admin

from .models import EmailAccount, EmailMessage


admin.site.register(EmailAccount)
admin.site.register(EmailMessage)