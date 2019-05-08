from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, Http404, JsonResponse

# Create your views here.

# accounts/views.py
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.template import loader, RequestContext
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic.detail import DetailView


from .models import CustomUser, FriendshipRequest, Chat, Friend

from django.http import HttpResponseRedirect



class UserProfileView(DetailView):
    model = CustomUser
    slug_field = "username"
    template_name = "profile.html"

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'logged_user': request.user})
    else:
        return HttpResponseRedirect('/login/')

def userlist(request):
    return render(request, 'users_mainpage.html', {'all_users': CustomUser.objects.all().values('username')})

def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/'+request.user.username+'/')
    else:
        form = CustomUserChangeForm()

    args['form'] = form
    args['logged_user']=request.user
    return render(request, 'update_profile.html', args)

def profile_page(request, string):

    try:
        user_fromUrl = CustomUser.objects.get(username = string)
    except Exception:
        raise Http404("User doesn't exist!")

    if request.is_ajax():


        if request.POST.get('from_accept'):

            to = user_fromUrl
            if to == request.user:
                from_name = request.POST.get('from_accept')
                from_ = CustomUser.objects.get(username = from_name)
                FriendshipRequest.objects.filter(to_user = to, from_user=from_ ).delete()
                add_friend(to, from_)
                return HttpResponse(from_)
            else:
                return HttpResponse('Unauthorized')

        elif request.POST.get('from_decline'):
            to = user_fromUrl
            if to == request.user:
                from_name = request.POST.get('from_decline')
                from_ = CustomUser.objects.get(username = from_name)
                FriendshipRequest.objects.filter(to_user = to, from_user=from_ ).delete()
                return HttpResponse(from_name)
            else:
                return HttpResponse('Unauthorized')

        elif request.POST.get('from_remove'):
            to = user_fromUrl
            if to == request.user:
                from_name = request.POST.get('from_remove')
                from_ = CustomUser.objects.get(username = from_name)
                remove_friend(to, from_)
                return HttpResponse(from_name)
            else:
                return HttpResponse('Unauthorized')

    logged_user = request.user
    if user_fromUrl.username == logged_user.username:

        if FriendshipRequest.objects.filter(to_user = logged_user).exists():
            f_requests = get_list_or_404(FriendshipRequest, to_user=logged_user)
        else:
            f_requests = list()

        if Friend.objects.filter(to_user = logged_user).exists():
            friends = get_list_or_404(Friend, to_user=logged_user)
        else:
            friends = list()

        return render(request, 'myprofile.html', {'user' : user_fromUrl, 'logged_user':logged_user,'Friends': friends, 'FriendRequest' : f_requests})
    else:
        return render(request, 'profile.html', {'user' : user_fromUrl, 'logged_user':logged_user })

def request_friendship(request,string):
    if(request.GET.get('friend_request')):
        friends = FriendshipRequest.objects.create(from_user=request.user, to_user = CustomUser.objects.get(username= string))
        friends.save()
        return HttpResponseRedirect('/')


def add_friend(user1, user2):
    friend1 = Friend.objects.create(to_user=user1, from_user=user2)
    friend2 = Friend.objects.create(to_user=user2, from_user=user1)
    friend1.save()
    friend2.save()
    return HttpResponse("")#profile_page(user_fromUrl.username)

def remove_friend(user1, user2):
    rem1 = Friend.objects.filter(from_user= user1, to_user=user2).delete()
    rem2 = Friend.objects.filter(from_user = user2, to_user= user1).delete()
    return HttpResponse("")



def chat_home(request):
    chats = Chat.objects.all()

    if request.user.is_authenticated:
        return render(request, 'chat.html', {'chat' : chats})
    else:
        return render(request, 'base.html', None )


def post(request):
    if request.method == "POST":
        msg = request.POST.get('chat-msg', '')
        print('Our value = ', msg)
        chat_message = Chat(user=request.user, message=msg)
        if msg != '':
            chat_message.save()
            return HttpResponseRedirect('/conversation/')
    else:
        return HttpResponse('Request must be POST.')


def messages(request):
    chat = Chat.objects.all()
    return render(request, 'messages.html', {'chat': chat})
