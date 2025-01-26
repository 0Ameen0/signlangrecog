from django.shortcuts import render

def index(request):
    return render(request,"index.html")

def admin(request):
    return render(request,"admin.html")

def login(request):
    return render(request,"login.html")
# Create your views here.
