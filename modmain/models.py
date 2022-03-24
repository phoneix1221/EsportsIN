from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from embed_video.fields import EmbedVideoField
from django.utils.timezone import now




class Tournament(models.Model):
    name=models.CharField(max_length=600,blank=False,default="")
    prize=models.IntegerField(default=0)
    entryfee=models.IntegerField(default=0)
    image=models.ImageField(default='default.png',upload_to='tournament_pics')
    winner_id=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    team_winner_id=models.ForeignKey("Team",blank=True,null=True,on_delete=models.SET_NULL)
    cover_image=models.ImageField(default='default.png',upload_to='tournament_cover_pics')
    gametype=models.ForeignKey("gamemodes", on_delete=models.CASCADE,blank=False)
    tournament_type=models.ForeignKey("tournamenttype",on_delete=models.CASCADE,blank=False)
    platform=models.ForeignKey("platform", on_delete=models.CASCADE,blank=False)
    game_id=models.ForeignKey('user.Game',on_delete=models.CASCADE,blank=False)
    total_no_of_players_or_team=models.IntegerField(blank=False)
    date_of_tournament=models.DateTimeField(blank=False)
    Description=models.TextField(blank=False)
    is_active=models.BooleanField(default=False)
    tournament_youtube_url=EmbedVideoField(blank=True)
    def __str__(self):
        return f'{self.name} Tournament Dated {self.date_of_tournament}'


class Participent(models.Model):
    Tournament_id=models.ForeignKey('Tournament',on_delete=models.CASCADE,default=False)
    User_id=models.ForeignKey(User,models.CASCADE,default=False)
    In_game_name=models.CharField(blank=False,default="",max_length=200)
    def __str__(self):
        return f'{self.Tournament_id} {self.User_id}'


class gamemodes(models.Model):
    gamemode=models.CharField(blank=False,max_length=100)
    def __str__(self):
        return f'{self.gamemode}'


class platform(models.Model):
    platform=models.CharField(blank=False,max_length=100)
    def __str__(self):
        return f'{self.platform}'


class tournamenttype(models.Model):
    gametype=models.CharField(blank=False,max_length=100)
    def __str__(self):
        return f'{self.gametype}'

class Team(models.Model):
    team_name=models.CharField(blank=False,max_length=100,unique=True)
    team_icon=models.ImageField(default='default.png',upload_to='team_pics')
    team_creator=models.ForeignKey(User,on_delete=CASCADE,blank=True,null=True)
    team_description=models.TextField(blank=True,max_length=500,null=True)
    team_player1=models.CharField(blank=True,max_length=100,null=True)
    team_player2=models.CharField(blank=True,max_length=100,null=True)
    team_player3=models.CharField(blank=True,max_length=100,null=True)
    team_player4=models.CharField(blank=True,max_length=100,null=True)
    date_of_creation=models.DateTimeField(blank=True,default=now)
    def __str__(self):
        return f'{self.team_name}'

class team_memeber_details(models.Model):
    team_id=models.ForeignKey("Team",on_delete=CASCADE)
    team_userid=models.ForeignKey(User,null=False,on_delete=CASCADE)
    verified=models.BooleanField(default=False,blank=True)
    date_of_request=models.DateTimeField(blank=True,default=now)
    def __str__(self):
        return f'{self.team_id}{"_"}{self.team_userid}'

    


    




    
