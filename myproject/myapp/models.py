from django.db import models

class Server(models.Model):
    serverID = models.CharField(max_length=100)
    serverName = models.CharField(max_length=100)

class User(models.Model):
    id =  models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    profileImage = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    isAdmin = models.BooleanField(default=False)
    isBanned = models.BooleanField(default=False)

class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE,  null=True, blank=True)
    messageType = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

