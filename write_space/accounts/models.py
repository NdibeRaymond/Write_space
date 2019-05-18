from django.db import models
from django.contrib.auth.models import User
from posts.models import Cartegory
from posts.models import Post
from django.urls import reverse

# Create your models here.
class userProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)

    #additional

    bio = models.CharField(max_length = 1000,blank = True)
    profile_pic = models.ImageField(upload_to = "images/profile_pics/",blank = True)
    background_pic = models.ImageField(upload_to = "images/background_pics/",blank = True)
    date_joined = models.DateTimeField(auto_now=True)
    follower = models.ManyToManyField("self",symmetrical=False)
    saved_for_future = models.ManyToManyField(Post,blank=True,related_name="saved")
    gender = models.CharField(max_length = 5,blank=False,default="")
    interests = models.ManyToManyField(Cartegory,blank=True)

    def __str__(self):
        return "@{}".format(self.user.username)


    def get_absolute_url(self):
        return reverse("accounts:user_profile",kwargs={"pk":self.pk,"username":self.user.username})

    def get_success_url(self):
        return HttpResponseRedirect(reverse_lazy(self.request.META.get('HTTP_REFERER')))
