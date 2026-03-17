from django.contrib import admin
from .models import User, Server, Message, Friend, FriendRequest

admin.site.register(User)
admin.site.register(Server)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(FriendRequest)
# Register your models here.
