from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=125)
    content = models.TextField(max_length=512) #Check the max length
    state = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    # After a blog has been created, where should the website take them
    def get_absolute_url(self):
        return reverse("my_app:detail", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    author = models.TextField(max_length=256)
    blog = models.ForeignKey(Blog, related_name='comments' , on_delete=models.CASCADE)
    content = models.TextField(max_length=512)
    status = models.BooleanField(default = False)
    # Add in create date for comment here

    def __str__(self) -> str:
        return self.author

    

