from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import requests
from requests.api import request
from .models import Tournament,team_memeber_details,Team
from django.views import generic 
from user.models import Game,Profile
from .forms import Participent_form,Team_form
from datetime import datetime
from django.contrib.auth.models import User
from notifications.signals import notify


# Create your views here.
def home(request):
    # response = requests.get('https://api.twitch.tv/helix/streams?game_id=32399', headers={'game_id':'32399','Client-ID':'i6q3bbk5a2dno33s2egw8qi4vdx16v','Authorization': 'Bearer 5p3ly9z4il9kczne7rq63yo4b7lm42'})
    # uppervideodata = response.json()
    # vid=[]
    # print(response.json())
    # for i in uppervideodata['data']:
    #     response1 = requests.get('https://api.twitch.tv/helix/videos?user_id='+i['user_id'], headers={'game_id':'32399','Client-ID':'i6q3bbk5a2dno33s2egw8qi4vdx16v','Authorization': 'Bearer d5xlnz8j0fco36kavjez9sb5vmv1ph'})
    #     res=response1.json()
        
    #     for j in res['data']:
    #         vid.append(j['id'])
    #         break
    #     break

    
    t_list=Tournament.objects.all().order_by('-date_of_tournament')
    g_list=Game.objects.all()
    
    context={'list':t_list,'glist':g_list}
    return render(request,"modmain/home.html",context)


def about(request):
    return render(request, "modmain/about.html")


class ModelNameDetail(generic.DetailView):
    model = Tournament
    template_name='modmain/tournament_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        t=context['tournament']
        try:
            context['is_registered']=t.participent_set.get(User_id=self.request.user)
        except :
            context['is_registered']=None
      
        return context



class gameDetailFilter(generic.DetailView):
    model = Game
    template_name='modmain/gamefilter.html'
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         
         t=context['game']
         try:
            context['tlist']=Tournament.objects.filter(game_id=t)
         except:
            context['tlist']=None 
            
         
         return context




@login_required
def register_tournament(request,pk):
    t=Tournament.objects.filter(id=pk).first()
    if request.method=='POST':
        form=Participent_form(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Tournament_id=Tournament.objects.filter(id=pk).first()
            instance.User_id=request.user
            form.save()
            us_obj=Profile.objects.get(user=request.user)
            us_obj.wallet=int(us_obj.wallet)-int(t.entryfee)
            us_obj.save()    

            return redirect('modmain-home')
            
    else:
        
        try:
            is_registered=t.participent_set.get(User_id=request.user)
        except :
            is_registered=None

        form = Participent_form()

        context={
            'form':form,
            'pk':pk,
            'is_registered':is_registered,
            'tournament':t,

        }
        return render(request,'modmain/Tournamentregister.html',context)

@login_required
def team_creation(request):
    if request.method == 'POST':
        form1 = Team_form(request.POST)
        data=form1
        if form1.is_valid():
            instance = form1.save(commit=False)
            instance.team_creator=request.user
            obj=Team.objects.create(team_name=instance.team_name,team_icon=instance.team_icon,team_creator=request.user,team_player1=instance.team_player1,team_player2=instance.team_player2,team_player3=instance.team_player3,team_player4=instance.team_player4)
            obj.save()
            # form1.save()
            # # if(instance.team_player1)
            try:
                us=User.objects.get(username=instance.team_player1)
                if us!=None:
                    team_memeber_details.objects.create(team_id=obj,team_userid=us)
                    notify.send(request.user, recipient=us, verb='Invited you to join his team : '+instance.team_name,action_object=obj)
            except:
                pass
            try:          
                us=User.objects.get(username=instance.team_player2)
                if us!=None:
                    team_memeber_details.objects.create(team_id=obj,team_userid=us)
                    notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=obj)
            except:
                pass 
            try:         
                us=User.objects.get(username=instance.team_player3)
                if us!=None:
                    team_memeber_details.objects.create(team_id=obj,team_userid=us)
                    notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=obj)
            except:
                pass
            try:  
                us=User.objects.get(username=instance.team_player4)
                if us!=None:
                    team_memeber_details.objects.create(team_id=obj,team_userid=us)
                    notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=obj)
            except:
                pass    




    form1=Team_form()
    data=request.user.notifications.unread()
    
    context={
        'form':form1,
        'data':data
    }
    return render(request,'modmain/team_creation.html',context)    



def notification(request):
    
    data=request.user.notifications.read()
   
    request.user.notifications.mark_all_as_read()
    
    context={
        'data':data,

    }
    
    return render(request,'modmain/notifications.html',context)



def pendinginvites(request):
    
    # data=request.user.notifications.unread()

    ar=[]
    # for i in data:
       
    #     if isinstance(i.action_object,Team):
            
    #         try:
    k=team_memeber_details.objects.filter(team_userid=request.user)
    for i in k:
        if i.verified==False:
                        
            ar.append(i)
            # except:
            #     pass
            
            
    
    context={
        'data':ar
    }
    return render(request,'modmain/pendingInvites.html',context)



def acceptinvitation(request,pk):

    obj=Team.objects.get(pk=pk)
    
    ik=team_memeber_details.objects.filter(team_id=obj,team_userid=request.user)
    for i in ik:
        
        i.verified=True
        i.save()
       
    return redirect("invites")


def deleteinvitation(request,pk):
    obj=Team.objects.get(pk=pk)
    ik=team_memeber_details.objects.filter(team_id=obj,team_userid=request.user)
    for i in ik:
        i.delete()
    ik.delete()
    return redirect("invites")



def TeamsDetail(request,pk):
    obj=Team.objects.get(pk=pk)
    
    if obj.team_creator==request.user:
        ls=True
    else:
        ls=False
    

    context={
        "data":obj,
        "check":ls
    }
    return render(request,'modmain/Team.html',context)


def TeamEdit(request,pk):
    if request.method=='POST':
        form=Team_form(request.POST)
        print("hii")
        
        if form.is_valid():
           
           
            instance = form.save(commit=False)
            cu=team_memeber_details.objects.filter(team_id=pk)
            
            for i in cu:
                if i.team_userid==instance.team_player1 or  i.team_userid==instance.team_player2 or  i.team_userid==instance.team_player3 or  i.team_userid==instance.team_player4:
                    print(i)
                   
                else:
                    print("deleted")
                    i.delete()
                    notify.send(request.user, recipient=i.team_userid, verb='Removed you from his team: '+instance.team_name)
            tm=Team.objects.get(pk=pk)
            tm.team_name=instance.team_name
            tm.team_icon=instance.team_icon
            
            tm.team_player1=instance.team_player1
            
            tm.team_player2=instance.team_player2
            
            tm.team_player3=instance.team_player3
            
            tm.team_player4=instance.team_player4
            tm.save()
            print("object saved")
            
            


            
            if instance.team_player1 in cu and instance.team_player1!=None:
                print("present")
            else:
                print("absent")
                print(instance.team_player1)
                
                try:          
                    us=User.objects.get(username=instance.team_player1)
                    if us!=None:
                        team_memeber_details.objects.create(team_id=tm,team_userid=us)
                        notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=tm)
                except:
                    pass
            if instance.team_player2 in cu:
                print("present")
            else:
                print("absent")
                print(instance.team_player2)
                try:          
                    us=User.objects.get(username=instance.team_player2)
                    if us!=None:
                        team_memeber_details.objects.create(team_id=tm,team_userid=us)
                        notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=tm)
                except:
                    pass
            if instance.team_player3 in cu:
                print("present")
            else:
                print("absent")
                print(instance.team_player3)
                try:          
                    us=User.objects.get(username=instance.team_player3)
                    if us!=None:
                        team_memeber_details.objects.create(team_id=tm,team_userid=us)
                        notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=tm)
                except:
                    pass
            if instance.team_player4 in cu:
               print("present")
            else:
                print("absent")
                print(instance.team_player4)
                try:          
                    us=User.objects.get(username=instance.team_player4)
                    if us!=None:
                        team_memeber_details.objects.create(team_id=tm,team_userid=us)
                        notify.send(request.user, recipient=us, verb='Invited you to join his team: '+instance.team_name,action_object=tm)

                except:
                    pass
                    
                    



            return redirect('modmain-home')
    else:
        form = Team_form(instance=Team.objects.get(pk=pk))
        context={
            'form':form
        }
        return render(request,'modmain/team_creation.html',context) 

    
