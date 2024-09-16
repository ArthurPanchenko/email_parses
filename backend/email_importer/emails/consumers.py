import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .email_services import fetch_emails
from .models import EmailMessage, EmailAccount


class EmailConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.email_id = self.scope['url_route']['kwargs']['email_id']
        self.email_account = await sync_to_async(self.get_email_account)(self.email_id)
        self.room_group_name = f'emails_{self.email_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.start_import()

    def get_email_account(self, pk):
        return EmailAccount.objects.get(pk=pk)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action', None)

        if action == 'start_importing':
            await self.start_import()

    async def start_import(self):
        last_sent_date = await sync_to_async(self.get_last_sent_date)()
        messages = await sync_to_async(fetch_emails)(self.email_account, last_sent_date)

        total_messages = len(messages)
        for index, email in enumerate(reversed(messages)):
            progress = (index + 1) / total_messages * 100
            status = f'Загружено {index + 1} из {total_messages} писем'

            data = {
                'progress': progress,
                'status': status,
                'email': email
            }
            text_data=json.dumps(data, default=str)
            await self.send(text_data)
            await self.save_email_to_db(email)    

    def get_last_sent_date(self):
        last_message = EmailMessage.objects.filter(email_account=self.email_account).order_by('-sent_date').first()
        return last_message.sent_date if last_message else None

    async def save_email_to_db(self, email):
        await sync_to_async(EmailMessage.objects.create)(
            email_account=self.email_account,
            subject=email['subject'],
            sent_date=email['sent_date'],
            body=email['body'],
            attachments=email['attachments']
        )