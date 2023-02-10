from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    likecount=serializers.CharField(read_only=True)
    
    class Meta:
        
        model=Comments
        fields=["id","comment","user","post","likecount"]

    def create(self, validated_data):
        ps=self.context.get("post")
        usr=self.context.get("user")
        return ps.comments_set.create(user=usr,**validated_data)


class PostsSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    post_cmts=CommentsSerializer(read_only=True,many=True)
    class Meta:
        model=Posts
        fields=["id","user","title","image","post_cmts"]
        
        
        
