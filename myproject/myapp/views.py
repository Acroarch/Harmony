from pyexpat.errors import messages
from urllib import request

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Message, Server
from datetime import datetime
from .models import User, Message, Server, FriendRequest, Friend
import json



@csrf_exempt
def home(request):
    if request.method == "GET":
        if not request.session.get("user_id"):  # ← checks if user_id exists in session
            return redirect("/log_in/")
        current_user = User.objects.get(id=request.session["user_id"])
        return render(request, "home.html", {"current_user": current_user})

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

def server_chat(request):
    if not request.session.get("user_id"):  # ← checks if user_id exists in session
            return redirect("/log_in/")
    
    current_user = User.objects.get(id=request.session["user_id"])
    print(current_user.userName)    
    harmony, created = Server.objects.get_or_create(id=1, defaults={"serverName": "Harmony"})
    messages =  Message.objects.filter(server=harmony).order_by("timestamp")[:50]

    if request.method =="POST":
        text = request.POST.get("message")
        m_sender = User.objects.get(id = request.session["user_id"])
        Message.objects.create(
            message = text,
            sender = m_sender,
            server = harmony,
            messageType = "Server",
            timestamp=datetime.now()
        )
        return redirect("/server/")
    return render(request, "server.html", {"messages": messages, "current_user": current_user, "test": "HELLO"})

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

def friends_list(request):
    if not request.session.get("user_id"):
        return redirect("/log_in/")
    current_user = User.objects.get(id=request.session["user_id"])
    friends = Friend.objects.filter(user=current_user)
    return render(request, "friends.html", {"current_user": current_user, "friends": friends})

def friend_requests(request):
    if not request.session.get("user_id"):
        return redirect("/log_in/")
    current_user = User.objects.get(id=request.session["user_id"])
    requests = FriendRequest.objects.filter(to_user=current_user)
    return render(request, "friend_requests.html", {"current_user": current_user, "requests": requests})

def handle_friend_request(request, request_id, action):
    if not request.session.get("user_id"):
        return redirect("/log_in/")
    freq = FriendRequest.objects.get(id=request_id)
    if action == "accept":
        Friend.objects.get_or_create(user=freq.from_user, friend=freq.to_user)
        Friend.objects.get_or_create(user=freq.to_user, friend=freq.from_user)
    freq.delete()
    return redirect("/friends/requests/")

def send_friend_request(request, user_id):
    if not request.session.get("user_id"):
        return redirect("/log_in/")
    current_user = User.objects.get(id=request.session["user_id"])
    to_user = User.objects.get(id=user_id)
    if current_user != to_user:
        FriendRequest.objects.get_or_create(from_user=current_user, to_user=to_user)
    return redirect("/server/")

def dm(request, user_id):
    if not request.session.get("user_id"):
        return redirect("/log_in/")
    current_user = User.objects.get(id=request.session["user_id"])
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(messageType="DM").filter(sender=current_user, receiver=other_user) | Message.objects.filter(
        sender=other_user, receiver=current_user).order_by("timestamp")

    if request.method == "POST":
        text = request.POST.get("message")
        Message.objects.create(
            message=text,
            sender=current_user,
            receiver=other_user,
            messageType="DM",
            timestamp=datetime.now()
        )
        return redirect(f"/dm/{user_id}/")

    return render(request, "dm.html", {"current_user": current_user, "other_user": other_user, "messages": messages})