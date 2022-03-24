from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.png',upload_to='profile_pics')
    phone_number=models.CharField( blank=True, null=True, default=None, unique=True,max_length=12)
    spoken_language=models.CharField(max_length=100)
    total_no_of_wins=models.IntegerField(default=0)
    wallet=models.IntegerField(default=0)
    level=models.IntegerField(default=0)
    

    def __str__(self):
        return f'{self.user.username} Profile'



class Game(models.Model):
    name=models.TextField()
    image=models.ImageField(default='default.png',upload_to='Games_pics')

    def __str__(self):
        return f'{self.name}'


class Favs(models.Model):
    gameid= models.ForeignKey(Game, on_delete=models.CASCADE)        
    userid= models.ForeignKey(User, on_delete=models.CASCADE)


class Accounts(models.Model):
    account_holder_id=models.ForeignKey(User,on_delete=models.CASCADE)
    account_number=models.CharField(max_length=12)
    account_holder_name=models.CharField(max_length=100)
    account_ifsc_code=models.CharField(max_length=11)
    bank_name=models.CharField(max_length=100)


class user_amount(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    payment_id=models.CharField(max_length=20)
    order_id=models.TextField()
    signature=models.TextField()
    is_successful=models.BooleanField(default=False)
    date_of_transcation=models.DateTimeField(blank=False)