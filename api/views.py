from django.shortcuts import render
from api.serializers import UserSerializer,PostsSerializer,CommentsSerializer
from api.models import Posts,Comments
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication,permissions
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class PostsView(ModelViewSet):
    serializer_class=PostsSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kw):
        qs=request.user.posts_set.all()
        serializer=PostsSerializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kw):
        id=kw.get("pk")
        ps=Posts.objects.get(id=id)
        usr=request.user
        serializer=CommentsSerializer(data=request.data,context={"post":ps,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    @action(methods=["GET"],detail=True)
    def list_comments(self,request,*args,**kw):
        id=kw.get("pk")
        ps=Posts.objects.get(id=id)
        cm=ps.comments_set.all()
        serializer=CommentsSerializer(cm,many=True)
        return Response(data=serializer.data)

class CommentsView(ModelViewSet):
    serializer_class=CommentsSerializer
    queryset=Comments.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    @action(methods=["GET"],detail=True)
    def like(self,request,*args,**kw):
        cmt=self.get_object()
        usr=self.request.user
        cmt.like.add(usr)
        return Response(data="liked")
