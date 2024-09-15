from django.db import models


class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
    

class EmailMessage(models.Model):
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    recieved_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True)
    attachments = models.JSONField(default=list)

    def __str__(self):
        return self.subject