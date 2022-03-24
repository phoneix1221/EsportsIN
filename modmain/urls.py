from django.urls import path
from . import views
from .views import ModelNameDetail,gameDetailFilter,team_creation,notification,pendinginvites,acceptinvitation,deleteinvitation,TeamsDetail,TeamEdit


urlpatterns = [
    path('', views.home,name="modmain-home"),
    path("about/",views.about,name="modmain-about"),
    path("game/<int:pk>/",gameDetailFilter.as_view(),name="games"),
    path("tournament/<int:pk>/Register",views.register_tournament,name="registertournament"),
    path('tournament/<int:pk>/',ModelNameDetail.as_view(),name="tournament_details"),
    path('CreateTeam/',team_creation,name="TeamCreation"),
    path('Notifications/',notification,name="notifications"),
    path('invites/',pendinginvites,name="invites"),
    path("acceptinvite/<int:pk>/",acceptinvitation,name="acceptinvite"),
    path("deleteinvite/<int:pk>/",deleteinvitation,name="deleteinvite"),
    path("Team/<int:pk>/",TeamsDetail,name="TeamDetails"),
    path("EditTeam/<int:pk>/",TeamEdit,name="EditTeam")

]
