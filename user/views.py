from modmain.views import team_creation
from django import forms
from django.http import response
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserProfileForm,Myamount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Game,Favs, Profile,user_amount
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from modmain.models import Tournament,Participent,Team,team_memeber_details
import razorpay
import datetime
from django.db.models import Q
from django.contrib.auth.models import User




def register(request):
    User._meta.get_field('email')._unique = True
    if request.user.is_authenticated:
        return redirect('modmain-home')

    formtitle=[
        "email",
        "username",
        "password",
        "confirm password"
    ]


    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            username = form.cleaned_data.get('username')
            # messages.success(request, f'Your Account has been created ! You can login now!')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('addprofiledetails')
    else:
        form = UserRegisterForm()
    return render(request, 'user/registration.html', {'form': form,"formtitle":formtitle})


@login_required
def profile(request):
    if request.method=='POST':
        form=UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
            
    else:
        form = UserProfileForm(instance=request.user.profile)
        t=Participent.objects.filter(User_id=request.user).count()
        k=team_memeber_details.objects.filter(team_userid=request.user).count()
        
        
       
        context={
            'form':form,
            'tot_match':t,
            'tot_teams':k,
        }
        return render(request,'user/profile.html',context)


def updateprofile(request):

    if request.method=='POST':
        form=UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('Favroutes')
        else:


            form = UserProfileForm(instance=request.user.profile)

            context={
                        'form':form,
                        'error':"phone number is already taken"
                    }
            messages.error(request, "Phone number already exist")
            return render(request, 'user/addprofiledetails.html',context)     

    else:
        form = UserProfileForm(instance=request.user.profile)

        context={
            'form':form
        }
        return render(request, 'user/addprofiledetails.html',context)





@csrf_exempt
def favroutes(request):
    if request.is_ajax():
        print(request)
        fotos = request.POST.getlist('array[]')
        
        for i in range(len(fotos)) :
            foo_instance = Favs.objects.create(gameid=Game.objects.get(id=fotos[i]),userid=request.user)
            foo_instance.save()
        print("redirect")
        return HttpResponse(status=204)
        

    # if request.method == 'POST':
    #     fotos = request.POST.getlist('arr1[]')
    #     for i in range(len(fotos)):
    #         print(fotos[i])
    #         print("hello")   
    #         print(Game.objects.first())  
    #         # foo_instance = Favs.objects.create(gameid=Game.objects.first(),userid=request.user)
    #         # foo_instance.save()  


    context={
            'data':Game.objects.all()
        }
    return render(request, 'user/addFavroutes.html',context)




# profile tournaments--------------------------------------------------

@login_required
def profile_tournaments(request):
    t=set()
    e=set()
    print(Participent.objects.filter(User_id=request.user))
    for e in Participent.objects.filter(User_id=request.user).select_related('Tournament_id'):
        t.add(e.Tournament_id)
        
    context={
            'data':t
        }
    return render(request, 'user/user_participate.html',context)


@login_required
def profile_wins(request):
    t=Tournament.objects.filter(winner_id=request.user)
        
    context={
            'data':t
        }
    return render(request, 'user/user_wins.html',context)





@login_required
def profile_wallet(request):
    client=razorpay.Client(auth=("rzp_test_9Ic6xTsM7UI2yT","uCbH4NyPtsiYZDKRIGG4CLNu"))
    t=Tournament.objects.filter(winner_id=request.user)
    transcation=user_amount.objects.filter(user_id=request.user).order_by('-date_of_transcation')
    form = Myamount(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            amount=form.cleaned_data.get('amount')
            
            payment=client.order.create({"amount":int(form.cleaned_data.get('amount')*100),'currency':'INR','payment_capture':'1'})
            context={
                'data':t,
                'form':form,
                'payment':payment,
                'trasnscation':transcation
            }
            pay_id=payment['id']
            pay_id=pay_id.strip()
            instance=user_amount(user_id=request.user,amount=amount,payment_id="",order_id=pay_id,signature="",date_of_transcation= datetime.datetime.now())
            instance.save()

            return render(request, 'user/wallet.html',context)
            
    context={
                'data':t,
                'form':form,
                'trasnscation':transcation
            }
    return render(request, 'user/wallet.html',context)


@csrf_exempt
def addmoney(request):
    if request.method=='POST':
        item=request.POST
        order_id=""
        signature=""
        pay_id=""

        for key,val in item.items():
            if key=="razorpay_order_id":
                order_id=val
            if key=="razorpay_signature":
                signature=val
            if key=="razorpay_payment_id":
                pay_id=val
      
        pay_id=str(pay_id.strip())
        if order_id is not None and signature is not None and pay_id is not None:
            obj=user_amount.objects.get(order_id=order_id)
            client=razorpay.Client(auth=("rzp_test_9Ic6xTsM7UI2yT","uCbH4NyPtsiYZDKRIGG4CLNu"))
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': pay_id,
                'razorpay_signature': signature
            }
            check=client.utility.verify_payment_signature(params_dict)
            if check:
                context={"result":"failed"}
                return render(request,'user/add_Money_success_failure.html',context)
            else:
                obj.payment_id=pay_id
                obj.signature=signature
                obj.is_successful=True
                obj.save()
                us_obj=Profile.objects.get(user=request.user)
                us_obj.wallet=int(us_obj.wallet)+int(obj.amount)
                us_obj.save()
                context={"result":"success",'order_id':order_id}  
                return render(request,'user/add_Money_success_failure.html',context)
        else:
            context={"result":"failed"}
            return render(request,'user/add_Money_success_failure.html',context)
    return render(request,'user/add_Money_success_failure.html')





def editprofile(request):

    if request.method=='POST':
        form=UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:


            form = UserProfileForm(instance=request.user.profile)

            context={
                        'form':form,
                        'error':"phone number is already taken"
                    }
            messages.error(request, "Phone number already exist")
            return render(request, 'user/edit_profile_details.html',context)     

    else:
        form = UserProfileForm(instance=request.user.profile)

        context={
            'form':form
        }

        


        return render(request, 'user/edit_profile_details.html',context)


def totalteams(request):
    ls=[]
    es=[]
    teamsmem=team_memeber_details.objects.filter(team_userid=request.user,verified=True)
    for i in teamsmem:
        teams=Team.objects.get(id=i.team_id.id)
        if teams.team_creator==request.user:
            es.append(True)
        else:
            es.append(False)    
        ls.append(teams)
        
    
    context={
        'data':zip(ls,es),
        'check':es
    }

    return render(request, 'user/TotalTeams.html',context)