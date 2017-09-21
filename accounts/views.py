import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from accounts.models import Token


def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def send_login_email(request):
    email = request.POST['email']
    uid = uuid.uuid4()
    Token.objects.create(email=email, uid=uid)
    print('Saving uid %s for email %s' % (uid, email), file=sys.stderr)
    url = request.build_absolute_uri('/accounts/login?uid=%s' % uid)
    send_mail(
        'Your login link for Superlists',
        'Please access the following link to access superlists \n\n%s' % (url),
        'Superlists Team',
        [email]
    )
    return render(request, 'login_email_sent.html')
