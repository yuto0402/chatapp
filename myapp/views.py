from django.shortcuts import redirect, render
from .forms import SignupForm

# Create your views here.

def index(request):
    return render (request, "myapp/index.html")

class SignUp(CreateView):
    form_class = SignupForm
    template_name = "myapp/signup.html" 
    # success_url = reverse_lazy('top')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト

# def signup(request):
#     form_class = SignupForm
#     user = form.save() # formの情報を保存
#     return render (request, "myapp/signup.html")

def login(request):
    return render (request, "myapp/login.html")

def friends(request):
    return render (request, "myapp/friends.html")

def talk_room(request):
    return render (request, "myapp/talk_room.html")

def setting(request):
    return render (request, "myapp/setting.html")
