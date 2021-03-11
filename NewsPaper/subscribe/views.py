from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime

from NewsPaper.base.models import Category, User

class SubscribeView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'subscribe.html',{})

