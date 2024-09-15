import imaplib
import email
from datetime import datetime
from email.utils import parsedate_to_datetime
from email.header import decode_header


def fetch_emails(email_account):
    mail = imaplib.IMAP4_SSL('imap.yandex.com', port=993)
    mail.login(email_account.email, email_account.password)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    messages = []

    for num in email_ids:
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        sent_date = parsedate_to_datetime(msg['Date'])
        
        body = ""
        attachments = []
        
        # Проверка на вложения
        if msg.is_multipart():
            for part in msg.walk():
                # Текст в body
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                # Вложения в attachments
                elif part.get("Content-Disposition") is not None:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
                        # Здесь можно сохранить файл
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        messages.append({
            'subject': subject,
            'sent_date': sent_date,
            'body': body,
            'attachments': []
        })
    return messages