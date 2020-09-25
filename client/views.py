from django.shortcuts import render
from .models import Category
# Create your views here.

def index(request):
    cats=Category.objects.all()
    return render(request,'client/home.html',{'cats':cats})