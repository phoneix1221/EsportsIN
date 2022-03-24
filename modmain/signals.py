from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from user.models import Profile
from .models import Tournament,Participent


@receiver(post_save,sender=Tournament)
def updateuserprofile(sender,instance,created,**kwargs):
    if created==False:
       if instance.winner_id!=None:
           us=instance.winner_id
           uprofile=us.profile
           uprofile.total_no_of_wins= uprofile.total_no_of_wins+1
           uprofile.wallet=uprofile.wallet+instance.prize
           uprofile.save()
           print("hii")

       else:
           print("hello-not updated")    

        

# @receiver(post_save,sender=User)
# def saveprofile(sender,instance,**kwargs):
#     instance.profile.save()