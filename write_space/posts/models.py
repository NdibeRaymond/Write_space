from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel,TreeForeignKey
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import cloudinary
import os

# Create your models here.
User = get_user_model()

class Post(models.Model):
    author= models.ForeignKey(User,on_delete = models.CASCADE,related_name="authors")
    title = models.CharField(max_length = 255,unique = True)
    main_image = models.TextField(blank=True,null=True)
    cartegory = TreeForeignKey('Cartegory',null=True,blank=True,on_delete = models.CASCADE,related_name="cartegories")
    clap = models.ManyToManyField(User,blank=True,related_name="claps")
    viewed = models.ManyToManyField(User,blank=True,related_name="viewed")
    post_heading = models.CharField(max_length = 120)
    text = models.TextField(blank = True, default = "")

    created_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    publish_date=models.DateTimeField(blank=True , null=True,default=None)

    def save(self,*args,**kwargs):
        print("save was called")
        print("the text",self.text)
        text = ""
        try:
            text = self.text.split("src=\"")[1].split("\"")[0]
        except:
            pass

        if text == "":
            pass
        else:
            self.main_image = text
            print("self.main_image was set",text)

        if self.slug:
            pass
        else:
            self.slug = slugify(self.title)
            print("self.slug was set",self.slug)

        super().save(*args,**kwargs)


    def publish(self):
        self.publish_date=timezone.now()
        self.save()

    def unpublish(self):
        self.publish_date=None
        self.save()


    def get_absolute_url(self):
        return reverse("posts:user_post_list",kwargs={"username":self.author})

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-created_at"]
        unique_together=["title","text"]



class Cartegory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    image = models.URLField(null=True,blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',db_index=True,on_delete = models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'cartegories'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs





class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE ,related_name="comments")
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(blank = True, default = "")
    created_at=models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("post_details",kwargs={"pk":self.pk})

    def __str__(self):
        return self.text
