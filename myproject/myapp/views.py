from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Message, Server
from datetime import datetime
from django.conf import settings



def check_active(request):
    return request.session.get("user_id")

def is_user_banned(user_id):
    try:
        user = User.objects.get(id=user_id)
        if(user.isBanned):
            return True
        return False  
    except User.DoesNotExist:
        return True
    
def redirect_for_inactive_and_banned(request):
    user_id = check_active(request)
    if is_user_banned(user_id):
        return redirect("/banned/")
    if not user_id:
        return redirect("/log_in/")
    return None


def your_banned_lol(request):
    if request.method == "GET":
        return render(request, "banned.html")
    
@csrf_exempt
def home(request):
    if request.method == "GET":
        redirect_response = redirect_for_inactive_and_banned(request)
        if redirect_response:
            return redirect_response
        return render(request, "home.html")

@csrf_exempt
def un_home(request):
    if request.method == "GET":
        return render(request, "harmony.html")
    

def log_out(request):
    redirect_response = redirect_for_inactive_and_banned(request)
    if redirect_response:
        return redirect_response
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
            if check_password(log_password, user.password):
                request.session["user_id"] = user.id
                return redirect("/home/")
            else:
                return render(request, "log_in.html", {"error": "Wrong Password"})
        except User.DoesNotExist:
            return render(request, "log_in.html", {"error": "User not found"})
    return render(request, "log_in.html")

def server_chat(request):
    redirect_response = redirect_for_inactive_and_banned(request)
    if redirect_response:
        return redirect_response
    else:
        harmony, created = Server.objects.get_or_create(
            id = 1,
            defaults={"serverName": "Harmony"}
        )
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
        return render(request, "server.html", {"messages":messages})
    
def edit_profile_page(request):
        if request.method == "GET":
            redirect_response = redirect_for_inactive_and_banned(request)
            if redirect_response:
                return redirect_response
            return render(request, "edit_profile_page.html")
        

def register_page(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password = request.POST.get("password")
        profileImage = request.FILES.get("profileImage")
        if User.objects.filter(userName=userName).exists():
            return render(request, "register.html", {"error": "Username already taken"}) 
        User.objects.create(
            userName= userName,
            password= make_password(password),
            profileImage = profileImage,
        ) 
        return redirect("/log_in/")  
    return render(request, "register.html")

def change_username(request):
    redirect_response = redirect_for_inactive_and_banned(request)
    if redirect_response:
        return redirect_response
    if request.method == "POST":
        user = User.objects.get(id = request.session["user_id"])
        new_userName = request.POST.get("userName")
        if User.objects.filter(userName=new_userName).exists():
                return render(request, "change_username.html", {"error": "Username already taken"}) 
        user.userName = new_userName
        user.save()
        return render(request, "change_username.html", {"success": "Username updated!"})  
    return render(request, "change_username.html")

def change_password(request):
    redirect_response = redirect_for_inactive_and_banned(request)
    if redirect_response:
        return redirect_response
    if request.method == "POST":
        user = User.object.get(id = request.session["user_id"])
        confirm_pass = request.POST.get("confPassword")
        new_pass = request.POST.get("newPassword")
        if(not check_password(confirm_pass, user.password)):
            return render(request, "change_password.html", {"error": "The entered current password is incorrect"})
        else:
            user.password = make_password(new_pass)
            user.save
            return render(request, "change_password.html", {"success": "Your password is now updated"})

    return render(request, "change_password.html")

def change_picture(request):
    redirect_response = redirect_for_inactive_and_banned(request)
    if redirect_response:
        return redirect_response
    user = User.objects.get(id=request.session["user_id"])
    if request.method == "POST":
        if "profileImage" in request.FILES:
            if user.profileImage:
                user.profileImage.delete()
            user.profileImage = request.FILES["profileImage"]
            user.save()
        elif "delete_image" in request.POST:
            if user.profileImage:
                user.profileImage.delete()        
                user.profileImage = None          
                user.save()
                return render(request, "change_picture.html", {"success": "Profile picture removed!"})
            else:
                return render(request, "change_picture.html", {"error" : "No profile picture to remove"})
    return render(request, "change_picture.html", {"user": user})