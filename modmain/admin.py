from django.contrib import admin
from .models import Tournament,Participent,gamemodes,platform,tournamenttype,team_memeber_details,Team
from .forms import Tournament_form


# Register your models here.

class TournamentModelAdmin(admin.ModelAdmin):
    form = Tournament_form
admin.site.register(Tournament,TournamentModelAdmin)
admin.site.register(Participent)
admin.site.register(gamemodes)
admin.site.register(platform)
admin.site.register(tournamenttype)
admin.site.register(team_memeber_details)
admin.site.register(Team)

