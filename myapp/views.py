from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, TalkRoom
from .forms import SignUpForm, LoginForm, TalkForm, ChangeForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, "myapp/index.html")

class signup_view(FormView):
    template_name = 'myapp/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignUpForm()
        return context    

class login_view(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"
    next_page = 'friends'

class friendList(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "myapp/friends.html"
    login_url = 'login_view'

    def get_queryset(self):
        query = self.request.GET.get('query')
        friend_list = self.request.user.followed_by.all().prefetch_related(
            Prefetch(
                'receiver', 
                queryset=TalkRoom.objects.filter(sender=self.request.user).order_by('-talkDate'),
                to_attr='last_received_message'
            ),
            Prefetch(
                'sender',
                queryset=TalkRoom.objects.filter(receiver=self.request.user).order_by('-talkDate'),
                to_attr='last_sent_message'
            )
        )
    
        if query:
            friend_list = friend_list.filter(Q(username__icontains=query) | Q(email__icontains=query))

        return friend_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_list = self.get_queryset()
        lastMessages = []
        for friend in friend_list:
            if friend.last_received_message:
                last_message = friend.last_received_message[0]
            elif friend.last_sent_message:
                last_message = friend.last_sent_message[0]
            lastMessages.append([friend, last_message])
        context['lastMessage'] = lastMessages
        return context

class talkRoom(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "myapp/talk_room.html" 

    def get_object(self, queryset=None):
        friend = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        self.messages = TalkRoom.objects.filter(
            (Q(sender=self.request.user) & Q(receiver=friend)) |
            (Q(receiver=self.request.user) & Q(sender=friend))
        ).select_related('sender', 'receiver').order_by('talkDate')
        return friend

    def post(self, request, *args, **kwargs):
        form = TalkForm(request.POST)
        friend = self.get_object()
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = friend
            message.save()
            return redirect('talk_room', pk=friend.pk)
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        friend = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['messages'] = self.messages
        context['form'] = TalkForm()
        context['friend'] = friend
        return context

class setting(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"

@login_required
def change_view(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('changeDone_view')
    else:
        form = ChangeForm(instance=user)
    return render(request, 'myapp/change.html', {'form': form})

class changeDone_view(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/changeDone.html'

class passwordChange_view(LoginRequiredMixin, PasswordChangeView):
    template_name = 'myapp/passwordChange.html'
    success_url = reverse_lazy('passwordChangeDone_view')

class passwordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/passwordChangeDone.html'

class logout_view(LoginRequiredMixin, LogoutView):
    next_page = 'index'