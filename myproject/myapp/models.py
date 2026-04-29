from django.db import models

class Server(models.Model):
    serverID = models.CharField(max_length=100)
    serverName = models.CharField(max_length=100)

class User(models.Model):
    id =  models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    profileImage = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    isAdmin = models.BooleanField(default=False) #create_superuser function will set this to True
    isBanned = models.BooleanField(default=False)

class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE,  null=True, blank=True)
    messageType = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"

