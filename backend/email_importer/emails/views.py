from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import EmailAccount, EmailMessage
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'emails/index.html')

def emails(request, pk):
    emails = EmailMessage.objects.filter(email_account__id=pk)
    return render(request, 'emails/emails.html', {
        'email_id': pk,
        'emails': emails
    })


@csrf_exempt
def import_emails(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'status': 'error', 'message': 'Email and password are required.'}, status=400)

            email, created = EmailAccount.objects.get_or_create(email=email, password=password)
            return JsonResponse({'status': 'success', 'email_id': email.id})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
