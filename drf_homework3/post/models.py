from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="post",blank=True,null=True)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="like_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, blank=True, null=True, related_name="comment")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="user_comment")
    content = models.CharField(max_length=300,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content