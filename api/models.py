from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
# Create your models here.


class Posts(models.Model):
    title=models.CharField(max_length=250)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    @property
    def post_cmts(self):
        return self.comments_set.all().annotate(u_count=Count('like')).order_by('u_count')
    
    def __str__(self):
        return self.title


class Comments(models.Model):
    comment=models.CharField(max_length=250)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="likes")
    @property
    def likecount(self):
        return self.like.all().count()

    def __str__(self):
        return self.comment


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField(auto_now_add=True)

