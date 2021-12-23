from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . models import Live_User,Room,Messages,Subscriptions
from django.http import HttpResponse, JsonResponse
import random,string
from datetime import datetime


def uniq_uid_gen():
    charset = string.digits
    res = ''.join(random.choices(charset, k=9))
    return 'DJC'+res

def rid_gen():
    charset = string.digits + string.ascii_lowercase
    res = ''.join(random.choices(charset, k=10))
    return res

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    subs = Subscriptions.objects.filter(lu_ref = Live_User.objects.get(user=request.user))
    user_room_details = []
    for s in subs:
        room = s.room_ref
        msgcount = Messages.objects.filter(date__gt=s.last_visited).count()
        # time_diff, lv = datetime.now()-s.last_visited, ''
        
        # if time_diff.days > 0:
        #     lv = lv+f'{time_diff.days} Days'
        # if time_diff.total_seconds() > 3600:
        #     lv=lv+ f'{time_diff.total_seconds()//3600} hours'
        # if time_diff.total_seconds() > 60:
        #     lv=lv+ f'{time_diff.total_seconds()//60} minutes' 
        # else:
        #     lv='Less than a Minute ago'

        user_room_details.append({
            'room':room,
            'msgcount':msgcount,
            'last_visited':s.last_visited
        })
    
    context = {'room_details':user_room_details, 'searched':''}

    searched_group = request.GET.get('search-input') or ''

    def filter_func(d):
        if searched_group in d['room'].name:
            return True
        else:
            return False

    if searched_group:
        context['room_details'] = filter(filter_func, context['room_details'])
        context['searched'] = searched_group

    return render(request, 'home.html', context=context)

def loginuser(request):
    if request.method == "POST":
        user_Name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=user_Name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'WELCOME '+ request.user.username +' to Django Chats !!')
            return redirect('/')
        else:
            # No backend authenticated the credentials
            if not User.objects.filter(username=user_Name).exists():
                messages.error(request, "No Such User is Found!! Please Register below..")
            elif User.objects.filter(username=user_Name)[0].password != password:
                messages.error(request, "Invalid Password !!")
            
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    messages.success(request, "You Have successfully Logged Out !!")
    return redirect('/login')

def register(request):
    if request.method == "POST":
        user_Name = request.POST.get('username')
        email = request.POST.get('email')
        dp = request.POST.get('dp')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if User.objects.filter(username=user_Name).exists():
            messages.info(request, 'This UserName is Already Taken !!')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This Email Address is Already Taken !!')
            
        else:
            if password == cpassword:
                user = User.objects.create_user(username=user_Name,email=email,password=password)
                uid = user.id
                user.save()
                
                luser = Live_User.objects.get(id=uid)
                luser.profile_pic = dp

                uuid = uniq_uid_gen()
                taken_uuid = [lus.uniq_userid for lus in Live_User.objects.all()] 
                while uuid in taken_uuid:
                    uuid = uniq_uid_gen()
                
                luser.uniq_userid = uuid
                luser.save()

                messages.success(request, "You are Successfully Registered!!")
                return render(request, 'register.html')
            else:
                messages.error(request, "Passwords Don't Match!!")
                return render(request, 'register.html')

    else:
        return render(request, 'register.html')

def checkroom(request):
    room_link = request.POST['room']

    if Room.objects.filter(room_id=room_link).exists(): 
        gdp = Room.objects.get(room_id=room_link).thumbnail
        if not gdp:
            gdp = "/media/thumbnails/w800.jpg"
        else:
            gdp = gdp.url

        room_data = {
            'r': Room.objects.get(room_id=room_link),
            'gdp': gdp
        }
        return render(request, 'room.html', context=room_data)
        

    elif Room.objects.filter(name=room_link).exists():
        gdp = Room.objects.get(name=room_link).thumbnail
        if not gdp:
            gdp = "/media/thumbnails/w800.jpg"
        else:
            gdp = gdp.url

        room_data = {
            'r': Room.objects.get(name=room_link),
            'gdp': gdp
        }
        return render(request, 'room.html', context=room_data)

    else:
        messages.error(request, "No Matching Room Exists, you can create a New Room rather.")
        return redirect('/')

    # else:
    #     new_room = Room.objects.create(name=room)
    #     new_room.save()
    #     return redirect('/'+room+'/?username='+username)

def createroom(request):
    room_Name = request.POST['room']

    if len(room_Name) and Room.objects.filter(name=room_Name).exists():
        rid = Room.objects.get(name=room_Name).room_id
        messages.error(request, "Room "+ room_Name.upper() +"' Already Exists.. !! Room ID; "+rid)
        return render(request, 'home.html')

    elif len(room_Name):
        rid = rid_gen()
        taken_rid = [r.room_id for r in Room.objects.all()] 
        while rid in taken_rid:
            rid = rid_gen()
                    
        new_room = Room.objects.create(name=room_Name, room_id=rid)
        new_room.save()

        messages.success(request, "New Room '"+ room_Name.upper() +"' Created !! Room ID; "+rid)
        return render(request, 'home.html')
    else:
        messages.error(request, "Please Give Us a Room-Name below..")
        return render(request, 'home.html')

def checkoutroom(request, room):
    r = Room.objects.get(room_id = room)
    u = Live_User.objects.get(user=request.user)

    if not Subscriptions.objects.filter(lu_ref=u, room_ref=r).exists():
        s = Subscriptions.objects.create(lu_ref=u, room_ref=r)
        s.save()
    else:
        s = Subscriptions.objects.get(lu_ref=u, room_ref=r)
        s.last_visited = datetime.now()
        s.save()
    
    return redirect('/')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Messages.objects.create(
        value = message, 
        date = datetime.now(),
        lu_ref = Live_User.objects.get(user=User.objects.get(username=username)),
        room_ref = Room.objects.get(room_id=room_id)
    )
    new_message.save()
    return HttpResponse("Message SENT !!!")

def getMessages(request, room):

    r = Room.objects.get(room_id=room)
    messages = Messages.objects.filter(room_ref=r)
    usernames,dp = [],[]
    for m in messages:
        usernames.append(m.lu_ref.user.username)
        dp.append(m.lu_ref.profile_pic.url)

    return JsonResponse({
        "messages":list(messages.values()),
        "usernames":usernames,
        "dp":dp,
    })