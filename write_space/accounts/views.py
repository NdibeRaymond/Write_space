from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from . import forms
from django.views import generic
from accounts import models
from posts.models import Cartegory,Post
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
import json


# Create your views here.


#########################################################
## used to implement the profile viewing functionality
######################################################
class profileView(LoginRequiredMixin,generic.TemplateView):
    login_url="/accounts/login/"
    template_name="accounts/user_profile.html"
    model=Post

    def get_context_data(self,**kwargs):
        all_posts = Post.objects.all()
        userprofiles=models.userProfile.objects.all()
        user = get_user_model().objects.get(username=self.kwargs.get("username"))
        try:
            user_posts = all_posts.filter(author=user)
        except:
            user_posts = []
        try:
            user_comments = all_posts.filter(comments__author=user)
        except:
            user_comments = []
        try:
            posts_viewed = all_posts.filter(viewed=user)
        except:
            posts_viewed = []
        try:
            following=userprofiles.filter(follower=user.userprofile)
        except:
            following = []
        context = super(profileView,self).get_context_data(**kwargs)
        context["user"] = user
        context["user_posts"] = user_posts
        context["user_comments"]=user_comments
        context["following"]=following
        context["posts_viewed"]=posts_viewed
        return context


#################################################
## allows a user to create a bio
#################################################
class Bio(LoginRequiredMixin,generic.UpdateView):
    login_url="/accounts/login/"
    template_name="accounts/my_bio_form.html"
    form_class=forms.bioForm
    model=models.userProfile


#################################################
## allows a user the view the available cartegories
#################################################
class interestView(LoginRequiredMixin,generic.DetailView):
    login_url="/accounts/login/"
    template_name="accounts/interests_page.html"
    model=models.userProfile
    context_object_name="user_interests"

    def get_context_data(self,**kwargs):
        user_interests = models.userProfile.objects.get(user__exact=get_user_model().objects.get(username__exact=self.kwargs.get("username"))).interests.all()
        context = super(interestView,self).get_context_data(**kwargs)
        context["user_interests"]=user_interests
        return context


################################################
## allows a user to follow another user
#############################################
@login_required
def follow_view(request,**kwargs):
    userprofile=models.userProfile.objects.get(pk=kwargs.get("pk"))
    if userprofile != request.user.userprofile:
        userprofile.follower.add(request.user.userprofile)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#################################################
## this views allows a user to see all the people they follow
#################################################
class Following(LoginRequiredMixin,generic.ListView):
    login_url="/accounts/login/"
    model = models.userProfile
    context_object_name = "people_you_follow"
    template_name = "accounts/following.html"

    def get_queryset(self,**kwargs):
        userprofiles = models.userProfile.objects.all()
        user = userprofiles.get(user = get_user_model().objects.get(username=self.kwargs.get("username")))
        people_you_follow = userprofiles.filter(follower=user)
        return people_you_follow


###################################################
## allows a user to unfollow another user
###################################################
@login_required
def unfollow_view(request,**kwargs):
    userprofile=models.userProfile.objects.get(pk=kwargs.get("pk"))
    if userprofile != request.user.userprofile:
        userprofile.follower.remove(request.user.userprofile)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


###########################################################
## allows a user to change their profile/background pic
###########################################################


@login_required
def change_profile_pic_view(request,**kwargs):

    if request.method == 'POST':
        user = models.userProfile.objects.get(user__exact=get_user_model().objects.get(username=kwargs.get("username")))
        data = request.POST.copy()
        profile_pic_url = data.get("profile_pic_url")
        background_pic_url = data.get("background_pic_url")
        print(profile_pic_url)
        print(background_pic_url)

        if (profile_pic_url != "" and profile_pic_url != None):
            user.profile_pic = "https://res.cloudinary.com/raymondndibe/"+profile_pic_url

        if (background_pic_url != "" and background_pic_url != None):
            user.background_pic = "https://res.cloudinary.com/raymondndibe/"+background_pic_url

        user.save()


        return HttpResponseRedirect(reverse_lazy("accounts:user_profile",kwargs={"username":kwargs.get("username"),"pk":kwargs.get("pk")}))

    else:

        return render(request,'accounts/change_profile_pic_form.html')




#############################################################
## allows a user to sign up to the platform
#############################################################
def signup(request):

    signedup = False

    if request.method == 'POST':
        print(request.POST["gender"])##########The solution
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        signup_form = forms.signupForm(data=request.POST)
        gender_form = forms.userGenderForm(data=request.POST)
        # Check to see both forms are valid
        if signup_form.is_valid() and gender_form.is_valid():

            # Save User Form to Database
            user = signup_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()
            user_gender=gender_form.save(commit=False)
            user_gender.user = user
            user_gender.save()
            # Registration Successful!
            signedup = True
            return HttpResponseRedirect(reverse_lazy("login"))

        else:
            # One of the forms was invalid if this else gets called.
            print(signup_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        signup_form = forms.signupForm()
        gender_form=forms.userGenderForm()

    return render(request,'accounts/signup.html',{'form':signup_form,'signedup':signedup,"gender_form":gender_form})




#####################################################
## allows a user to select his or her cartegory interests
#####################################################
@login_required
def selectinterest(request):

    interestselected = False
    if request.method == 'POST':
        #assigns the selected cartegories and the user instance to the interestSelectForm
        interest_select_form = forms.interestSelectForm(data=request.POST,instance=request.user)

        #checks if the interest form is valid
        if interest_select_form.is_valid():
            user=interest_select_form.save(commit=False)
            #gets the actual list of interests from the request.POST
            interests = request.POST.getlist('interests')
            #iterate through them and add all of them to the user.userprofile.interests in the userprofile model
            for each_pk in interests:
                user.userprofile.interests.add(Cartegory.objects.get(id=each_pk))
            interestselected = True
            return HttpResponseRedirect(reverse_lazy("accounts:select_pic"))
            # return redirect("accounts:select_pic")
        else:
            print(interest_select_form.errors)
    else:
        if request.user.is_active:
            user_profile_query = models.userProfile.objects.get(user__exact=request.user)
            if user_profile_query.interests.all():
                print(user_profile_query.interests,"interests already selected")
                # return HttpResponseRedirect(reverse("accounts:select_pic"))
                return redirect("accounts:select_pic")
            else:
                print(user_profile_query.interests,"no interests selected yet")
        else:
            pass
        interest_select_form = forms.interestSelectForm()
    return render(request,'accounts/choose_interests_page.html',{'form':interest_select_form,'interestselected':interestselected})
#


######################################################
## allows a user to choose a profile picture
######################################################
@login_required
def selectprofilepicture(request):
    profilepictureselected = False
    profile=request.user

    if request.method == 'POST':
        # #assigns the selected profile picture and the user instance to the profilePicSelectForm
        # profile_pic_select_form = forms.profilePicSelectForm(data=request.POST,instance=request.user)
        # #check if the selected picture is valid
        # if profile_pic_select_form.is_valid():
        #     user_pic = profile_pic_select_form.save(commit=False)
        #
        #     if 'profile_pic' in request.FILES:
        #         # If yes, then grab it from the POST form reply
        #         user_pic.userprofile.profile_pic = request.FILES['profile_pic']
        #
        #     # Now save model
        #     user_pic.userprofile.save()
        user = models.userProfile.objects.get(user__exact=request.user)
        data = request.POST.copy()
        profile_pic_url = data.get("profile_pic_url")
        background_pic_url = data.get("background_pic_url")
        print(profile_pic_url)
        print(background_pic_url)

        if (profile_pic_url != "" and profile_pic_url != None):
            user.profile_pic = "https://res.cloudinary.com/raymondndibe/"+profile_pic_url

        if (background_pic_url != "" and background_pic_url != None):
            user.background_pic = "https://res.cloudinary.com/raymondndibe/"+background_pic_url

        user.save()

        profilepictureselected = True

        return HttpResponseRedirect(reverse_lazy("posts:post_list"))


        #     return HttpResponseRedirect(reverse_lazy("posts:post_list"))
        # else:
        #     print(profile_pic_select_form.errors)
    else:
        if request.user.is_active:

            user_profile_query = models.userProfile.objects.get(user__exact=request.user)
            if user_profile_query.profile_pic:
                print(user_profile_query.profile_pic,"profile picture already selected")

                return redirect("posts:post_list")
            else:
                print(user_profile_query.profile_pic,"no profile picture selected yet")
        else:
            pass
    return render(request,'accounts/choose_profile_pic_page.html')
