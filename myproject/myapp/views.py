from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import json



@csrf_exempt
def home(request):
    if request.method == "GET":
        if not request.session.get("user_id"):  # ← checks if user_id exists in session
            return redirect("/log_in/")
        return render(request, "home.html")

@csrf_exempt
def un_home(request):
    if request.method == "GET":
        return render(request, "harmony.html")

def log_out(request):
    if not request.session.get("user_id"):  # ← checks if user_id exists in session
        return redirect("/log_in/")
    else:
        del request.session["user_id"]
        return redirect("/")
    
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        log_userName = request.POST.get("userName")
        log_password = request.POST.get("password")
        try:
            user = User.objects.get(userName= log_userName)
            request.session["user_id"] = user.id
            if check_password(log_password, user.password):
                return redirect("/home/")
            else:
                return render(request, "log_in.html", {"error": "Wrong Password"})
        except User.DoesNotExist:
            return render(request, "log_in.html", {"error": "User not found"})
    return render(request, "log_in.html")


def register_page(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password = request.POST.get("password")
        if User.objects.filter(userName=userName).exists():
            return render(request, "register.html", {"error": "Username already taken"}) #adds message at the top of the html page
        User.objects.create(
            userName=userName,
            password=make_password(password),
            isAdmin=False
        ) #adds to database User.objects
        return redirect("/log_in/")  
    return render(request, "register.html")