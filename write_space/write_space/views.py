from django.views import generic
from django.urls import reverse_lazy,reverse
from accounts.models import userProfile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json
import cloudinary


class LandingPage(generic.RedirectView):


    def get_redirect_url(self):
        return reverse("posts:post_list")


class aboutView(generic.TemplateView):
    template_name="about.html"

@login_required
def delete_image_async(request,**kwargs):
    print("delete image async was called")
    username = kwargs.get("username")
    pk = kwargs.get("pk")
    folder = kwargs.get("folder")
    public_id = kwargs.get("public_id")
    image_type = kwargs.get("type")
    print(public_id)

    result = cloudinary.uploader.destroy(public_id=folder+"/"+public_id,resource_type="image",invalidate=True)
    print(result)
    if(result["result"] == "ok" or result["result"] == "not found"):
        user = userProfile.objects.get(user = get_user_model().objects.get(username=username))
        print(user.profile_pic,user.background_pic)
        if(image_type == "profile_pic"):
            user.profile_pic = None
        elif(image_type == "background_pic"):
            user.background_pic = None
        # elif(image_type == "post_pic"):
        #     ....
        # elif(image_type == "cartegory_pic"):
        #     ...
        user.save()


    return JsonResponse(result)
