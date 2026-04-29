from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from .models import User, Message, Server, FriendRequest, Friend

from functools import wraps

def is_user_banned(user_id):
    try:
        user = User.objects.get(id=user_id)
        if(user.isBanned):
            return True
        return False  
    except User.DoesNotExist:
        return False

def login_and_active_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("/log_in/")
        try: #this is the checkActive def I deleted - Jerry
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            del request.session["user_id"]
            return redirect("/log_in/")
        if user.isBanned:
            return redirect("/banned/")
        return view_func(request, *args, **kwargs)
    return wrapper


def your_banned_lol(request):
    if request.method == "GET":
        return render(request, "banned.html")
    
@login_and_active_required #this replaced all the  if not request.session.get("user_id"):checks if user_id exists in session
def home(request):
    if request.method == "GET":
        current_user = User.objects.get(id=request.session["user_id"])
        friends = Friend.objects.filter(user=current_user)

        return render(request, "home.html", {"current_user": current_user, "friends": friends})


def un_home(request): #for users not logged in, to see the homepage with the server chat but no messages or friends list
    if request.method == "GET":
        return render(request, "harmony.html")


def log_out(request):
    request.session.pop("user_id", None)
    return redirect("/")

    
def login_user(request): 
    if request.method == "POST":
        log_userName = request.POST.get("userName")
        log_password = request.POST.get("password")
        try:
            user = User.objects.get(userName=log_userName)
            if check_password(log_password, user.password):
                if user.isBanned:
                    return render(request, "log_in.html", {"error": "Your account has been banned."})
                request.session["user_id"] = user.id
                return redirect("/home/")
            else:
                return render(request, "log_in.html", {"error": "Wrong Password"})
        except User.DoesNotExist:
            return render(request, "log_in.html", {"error": "User not found"})
    return render(request, "log_in.html")

@login_and_active_required
def server_chat(request):

    current_user = User.objects.get(id=request.session["user_id"])
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
    friends = Friend.objects.filter(user=current_user)
    return render(request, "server.html", {"messages": messages, "current_user": current_user, "friends": friends})

def register_page(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password = request.POST.get("password")
        if User.objects.filter(userName=userName).exists():
            return render(request, "register.html", {"error": "Username already taken"}) #adds message at the top of the html page
        user = User.objects.create(
            userName=userName,
            password=make_password(password),
            isAdmin=False
        )
        if request.FILES.get("profileImage"):
            user.profileImage = request.FILES["profileImage"]
            user.save()
        return redirect("/log_in/")  
    return render(request, "register.html")

@login_and_active_required
def friends_list(request):
    current_user = User.objects.get(id=request.session["user_id"])
    friends = Friend.objects.filter(user=current_user)
    return render(request, "friends.html", {"current_user": current_user, "friends": friends})

@login_and_active_required
def friend_requests(request):
    current_user = User.objects.get(id=request.session["user_id"])
    friends = Friend.objects.filter(user=current_user)
    requests = FriendRequest.objects.filter(to_user=current_user)
    return render(request, "friend_requests.html", {"current_user": current_user, "requests": requests, "friends": friends})

@login_and_active_required
def handle_friend_request(request, request_id, action):
    freq = FriendRequest.objects.get(id=request_id)
    if action == "accept":
        Friend.objects.get_or_create(user=freq.from_user, friend=freq.to_user)
        Friend.objects.get_or_create(user=freq.to_user, friend=freq.from_user)
    freq.delete()
    if action == "accept":
        return redirect("/friends/")
    return redirect("/friends/requests/")

@login_and_active_required
def send_friend_request(request, user_id):
    current_user = User.objects.get(id=request.session["user_id"])
    to_user = User.objects.get(id=user_id)
    if current_user != to_user:
        FriendRequest.objects.get_or_create(from_user=current_user, to_user=to_user)
    return redirect("/server/")

@login_and_active_required
def direct_messages(request, user_id):
    current_user = User.objects.get(id=request.session["user_id"])
    other_user = get_object_or_404(User, id=user_id)
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
        return redirect(f"/direct_messages/{user_id}/")

    friends = Friend.objects.filter(user=current_user)
    return render(request, "direct_messages.html", {"current_user": current_user, "other_user": other_user, "messages": messages, "friends": friends})

@login_and_active_required
def edit_profile(request):
    current_user = User.objects.get(id=request.session["user_id"])
    friends = Friend.objects.filter(user=current_user)

    if request.method == "POST":
        new_userName = request.POST.get("userName")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if new_userName:
            current_user.userName = new_userName
        if new_password:
            if new_password == confirm_password:
                current_user.password = make_password(new_password)
            else:
                return render(request, "edit_profile.html", {"current_user": current_user, "friends": friends, "error": "Passwords do not match"})
        if request.FILES.get("profileImage"):
            current_user.profileImage = request.FILES["profileImage"]
        current_user.save()
        return redirect("/home/")

    return render(request, "edit_profile.html", {"current_user": current_user, "friends": friends})

    

@login_and_active_required
def create_superuser(request):
    user = User.objects.get(id=request.session["user_id"])

    if not user.isAdmin:
        return redirect("/home/")

    if request.method == "POST":
        from django.contrib.auth.models import User as DjangoUser
        new_password = request.POST.get("new_password")
        if DjangoUser.objects.filter(username=user.userName).exists():
            return render(request, "create_superuser.html", {"error": "Superuser already exists for this account"})

        DjangoUser.objects.create_superuser(
            username=user.userName,
            password=new_password,
            email=""
        )
        return render(request, "create_superuser.html", {"success": "Superuser created! You can now log into /admin/"})

    return render(request, "create_superuser.html")