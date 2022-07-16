from django.shortcuts import render
from .models import News


def home_view(request):
  news = News.objects.all()
  return render(request, "test.html", {'news': news})

