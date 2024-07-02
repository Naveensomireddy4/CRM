from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#whenever a user is created corresponding userprofile 
#should be creates .To do this we have Signals in django
#Signals are events that are fired when certain action takes place
from django.db.models.signals import post_save,pre_save
#pre_saveto add new information before saving to database
#post_save add new information after saving to database

class User(AbstractUser):
    
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)



class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return self.user.username
class Lead(models.Model):


    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent",on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Agent(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
    
    
def post_user_created_signal(sender , instance , created, **kwargs):
    print(instance, created)
    if created :
        UserProfile.objects.create(user=instance)
    
post_save.connect(post_user_created_signal,sender = User)    