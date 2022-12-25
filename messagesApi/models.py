from django.db import models
from django.contrib.auth.models import User
import datetime

class Message(models.Model):
    sender = models.ForeignKey(User,related_name= "sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name= "receiver",on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    subject = models.CharField(max_length=100)
    creationDate = models.DateTimeField(default=datetime.datetime.now, blank=True)
    HasBeenRead = models.BooleanField(default=False)
    

    def __str__(self):
        return "Message - {} :from {} to {} - {}".format(self.id,self.sender,self.receiver,self.subject)