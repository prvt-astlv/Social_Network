from django.shortcuts import render
from . import models
from accounts.models import Profile
from .forms import MessageForm


# Create your views here.
def ChatView(request):
    profiles = Profile.objects.all()
    profs = []
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile in request.user.profile.follows.all():
            profs.append(profile)
    return render(request, 'chat_dashboard.html', context={'profiles': profs})



def ChattingView(request, pk):
    sender = Profile.objects.get(user=request.user)
    receiver = Profile.objects.get(pk=pk)
    form = MessageForm()
    messages = models.Message.objects.filter(sender=sender, receiver=receiver)
    if request.method == "POST":
        msg = request.POST.get('body', None)
        c = models.Message(body=msg, sender=sender, receiver=receiver)
        if msg != '':
            c.save()
    return render(request, 'chat.html', context={'form': form, "messages": messages, 'receiver': receiver})
