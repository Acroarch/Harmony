from django.contrib import admin
from .models import User, Server, Message

admin.site.register(User)
admin.site.register(Server)
admin.site.register(Message)
# Register your models here.
