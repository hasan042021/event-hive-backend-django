from django.urls import get_resolver
from django.http import HttpResponse
from django.shortcuts import render


def home(request):

    return render(request, "home.html")
