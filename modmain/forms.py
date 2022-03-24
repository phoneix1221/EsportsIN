from django import forms
from django.contrib.auth.models import User
from .models import Participent, Tournament,Team,team_memeber_details

class Participent_form((forms.ModelForm)):
     class Meta:
        model=Participent
        fields=['In_game_name']


class Tournament_form(forms.ModelForm):
   class Meta:
        model = Tournament
        
        fields = [
            "name",
            "prize",
            "entryfee",
            "image",
            "cover_image",
            "gametype",
            "tournament_type",
            "platform",
            "game_id",
            "winner_id",
            "total_no_of_players_or_team",
            "date_of_tournament",
            "Description",
            "is_active",
            "tournament_youtube_url"

        ]

   def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         instance = kwargs.get("instance")
         t=set()
         k=set()
         if instance:
            f=Participent.objects.filter(Tournament_id=instance.pk)
            for e in Participent.objects.filter(Tournament_id=instance.pk).select_related('User_id'):
               t.add(e.User_id)

         for i in t:
            k.add(i.id)

         
         self.fields['winner_id'].queryset=User.objects.filter(pk__in=k)



class Team_form(forms.ModelForm):
   class Meta:
      model=Team
      labels = {
        "team_player1": "First Player Username",
        "team_player2":" Second Player Username",
        "team_player3":"Third Player Username",
        "team_player4":"Foruth Player Username"
      }
      fields=['team_name','team_icon','team_player1','team_player2','team_player3','team_player4']
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_name'].widget.attrs.update({'placeholder': 'Team Name'})
        self.fields['team_icon'].widget.attrs.update({'placeholder': 'Team Icon'})
        self.fields['team_player1'].widget.attrs.update({'placeholder': 'Player name'})
        self.fields['team_player2'].widget.attrs.update({'placeholder': 'Player name'})
        self.fields['team_player3'].widget.attrs.update({'placeholder': 'Player name'})
        self.fields['team_player4'].widget.attrs.update({'placeholder': 'Player name'})

# class team_member_form(forms.ModelForm):
#    class Meta:
#       model=team_memeber_details
#       fields=['team_userid']
#       def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['team_userid'].widget.attrs.update({'placeholder': 'Username'})


