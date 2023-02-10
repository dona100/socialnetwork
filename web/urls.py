from django.urls import path
from .views import SignInView,SignUpView,IndexView,add_comment,post_like_view,signout_view,ListPeopleView,add_follower,PostView,ProfileView

urlpatterns = [
    path("",SignInView.as_view(),name="signin"),
    path("register",SignUpView.as_view(),name="signup"),
    path("index",IndexView.as_view(),name="index"),
    path("post",PostView.as_view(),name="post"),
    path("profile",ProfileView.as_view(),name="profile"),
    path("posts/<int:id>/comments/add",add_comment,name="add-comment"),
    path("comments/<int:id>/likes/add",post_like_view,name="add-like"),
    path("user/<int:id>/follower/add", add_follower, name="add-follower"),
    path("people/", ListPeopleView.as_view(), name="people"),
    path("logout",signout_view,name="sign-out")
]
