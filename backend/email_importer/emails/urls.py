from django.urls import path
from .views import index, emails, import_emails

urlpatterns = [
    path('', index, name='index'),
    path('emails/<int:pk>/', emails, name='email_list'),
    path('import/', import_emails, name='import_emails'),
]
