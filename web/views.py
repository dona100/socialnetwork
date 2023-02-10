from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView
from .forms import LoginForm,UserRegistrationForm,PostForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from api.models import Posts,Comments,User,Friends
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decs=[signin_required,never_cache]

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    success_url=reverse_lazy("index")
    model=Posts
    context_object_name="posts"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Posts.objects.order_by("-created_date")

@method_decorator(decs,name="dispatch")
class PostView(CreateView):
    template_name="post.html"
    form_class=PostForm
    success_url=reverse_lazy("index")
    model=Posts
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class ProfileView(TemplateView):
    template_name="profile.html"
    
class ListPeopleView(ListView):
    template_name="people/peoples.html"
    model = User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")


def add_comment(request,*args,**kw):
    id=kw.get("id")
    pst=Posts.objects.get(id=id)
    cmt=request.POST.get("comment")
    Comments.objects.create(post=pst,comment=cmt,user=request.user)
    return redirect("index")

def post_like_view(request,*args,**kw):
    id=kw.get("id")
    cm=Comments.objects.get(id=id)
    cm.like.add(request.user)
    return redirect("index")

def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")