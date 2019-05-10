from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse,reverse_lazy
from . import forms
from django.views import generic
from accounts import models
from posts.models import Cartegory,Post
from django.forms import ChoiceField
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import CreateView


# Create your views here.

class profileView(LoginRequiredMixin,generic.TemplateView):
    login_url="/accounts/login/"
    template_name="accounts/user_profile.html"
    # context_object_name="posts"
    model=Post
    # def get_queryset(self,**kwargs):
    #     post=Post.objects.filter(author=get_user_model().objects.get(pk=self.kwargs.get("pk")))
    #     return post

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



class Bio(LoginRequiredMixin,generic.UpdateView):
    login_url="/accounts/login/"
    template_name="accounts/my_bio_form.html"
    form_class=forms.bioForm
    model=models.userProfile

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

# class followView(generic.UpdateView):
#     # template_name="accounts/user_profile.html"
#     # context_object_name="user"
#     # success_url = reverse_lazy("accounts:user_profile")
#     model= get_user_model()
#
#     def get_context_data(self,**kwargs):
#         userprofile=models.userProfile.objects.get(pk=get_user_model().objects.get(pk=self.kwargs.get("pk")))
#         userprofile.follower.add(self.request.user.userprofile)
#         # userprofiles=models.userProfile.objects.all()
#         # following=userprofiles.filter(follower=userprofile)
#         context = super(followView,self).get_context_data(**kwargs)
#         # context["user"]=get_user_model().objects.get(username__exact=self.kwargs.get("username"))
#         # context["following"]=following
#         return context
#     def get_success_url(self):
#         return HttpResponseRedirect(reverse_lazy(self.request.META.get('HTTP_REFERER')))
#
#
# class unfollowView(generic.UpdateView):
#     # template_name="accounts/user_profile.html"
#     # context_object_name="user"
#     # success_url = reverse_lazy("accounts:user_profile")
#     model=get_user_model()
#
#     def get_context_data(self,**kwargs):
#         print(self.kwargs)
#         userprofile=models.userProfile.objects.get(pk=get_user_model().objects.get(pk=self.kwargs.get("pk")))
#         userprofile.follower.remove(self.request.user.userprofile)
#
#         # userprofiles=models.userProfile.objects.all()
#         # following=userprofiles.filter(follower=userprofile)
#         context = super(unfollowView,self).get_context_data(**kwargs)
#         # context["user"]=get_user_model().objects.get(username__exact=self.kwargs.get("username"))
#         # context["following"]=following
#         return context
#     def get_success_url(self):
#         return HttpResponseRedirect(reverse_lazy(self.request.META.get('HTTP_REFERER')))
@login_required
def follow_view(request,**kwargs):
    userprofile=models.userProfile.objects.get(pk=kwargs.get("pk"))
    if userprofile != request.user.userprofile:
        userprofile.follower.add(request.user.userprofile)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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



@login_required
def unfollow_view(request,**kwargs):
    userprofile=models.userProfile.objects.get(pk=kwargs.get("pk"))
    if userprofile != request.user.userprofile:
        userprofile.follower.remove(request.user.userprofile)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class changeProfilePicView(LoginRequiredMixin,generic.UpdateView):
    login_url="/accounts/login/"
    template_name="accounts/change_profile_pic_form.html"
    form_class=forms.profilePicSelectForm
    model=models.userProfile

# @login_required
# def changeprofilepicture(request):
#     profilepictureselected = False
#     # profile=get_object_or_404(request.user.userprofile,pk=pk)
#     profile=request.user.userprofile
#
#     if request.method == 'POST':
#         profile_pic_select_form = forms.profilePicSelectForm(data=request.POST,instance=profile)
#         # ChoiceField.clean(forms.userGenderForm(),gender_form)
#         # print(cleaned_gender_form)
#         if profile_pic_select_form.is_valid():
#             user_pic = profile_pic_select_form.save(commit=False)
#
#             if 'profile_pic' in request.FILES:
#                 print('found it')
#                 print(user_pic)
#                 # print(request.FILES)
#                 # print(user_pic.userprofile.profile_pic)
#                 # If yes, then grab it from the POST form reply
#                 user_pic.profile_pic = request.FILES['profile_pic']
#
#             # Now save model
#             user_pic.save()
#
#             profilepictureselected = True
#             print(profilepictureselected)
#
#             return reverse_lazy(profile.get_absolute_url())
#         else:
#             print(profile_pic_select_form.errors)
#     else:
#         profile_pic_select_form = forms.profilePicSelectForm()
#     return render(request,'accounts/change_profile_pic_form.html',{'form':profile_pic_select_form,'profilepictureselected':profilepictureselected})
#



def signup(request):

    signedup = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        signup_form = forms.signupForm(data=request.POST)
        gender_form = forms.userGenderForm(data=request.POST)
        # ChoiceField.clean(forms.userGenderForm(),gender_form)
        # print(cleaned_gender_form
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



            # set a onetoone relationship between userprofileinfo model and get_user_model() model
            # models.userProfile.objects.create(user=get_user_model().objects.get(username__iexact=user.username)).save()




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
#


# class signUp(CreateView):
#     success_url=reverse_lazy("login")
#     template_name="accounts/signup.html"
#
#     def get_context_data(self,**kwargs):
#         context = super(signUp,self).get_context_data(**kwargs)
#         context["form"] = forms.signupForm
#         context["gender_form"]=forms.userGenderForm
#         return context


# class selectInterest(LoginRequiredMixin,generic.CreateView):
#     form_class=forms.interestSelectForm
#
#     template_name="accounts/choose_interests_page.html"
#
#     def get_queryset(self):
#         if self.request.user.is_active:
#             try:
#                 self.user_profile_query = models.userProfile.objects.get(user_exact=self.request.user)
#                 if self.user_profile_query.interests:
#                     print(self.user_profile_query.interests,"interests already selected")
#
#                 else:
#                     print(self.user_profile_query.interests,"no interests selected yet")
#             except:
#                 pass
#
#
#     def get_context_data(self,**kwargs):
#         context = super(selectInterest,self).get_context_data(**kwargs)
#         try:
#             context["user_profile"] = models.userProfile.objects.get(user_exact=self.request.user)
#         except:
#             pass
#         return context


# class selectProfilePicture(LoginRequiredMixin,generic.CreateView):
#     form_class=forms.profilePicSelectForm
#     success_url=reverse_lazy("selectprofilepicture")
#     template_name="accounts/choose_profile_pic_page.html"
#
#     def get_queryset(self):
#         if self.request.user.is_active:
#             try:
#                 self.user_profile_query = models.userProfile.objects.get(user_exact=self.request.user)
#                 if self.user_profile_query.profile_pic:
#                     print(self.user_profile_query.profile_pic,"profile picture already selected")
#                     HttpResponseRedirect(reverse("selectprofilepicture"))
#                 else:
#                     print(self.user_profile_query.profile_pic,"no profile picture selected yet")
#             except:
#                 pass
#
#
#     def get_context_data(self,**kwargs):
#         context = super(selectProfilePicture,self).get_context_data(**kwargs)
#         try:
#             context["user_profile"] = models.userProfile.objects.get(user_exact=self.request.user)
#         except:
#             pass
#         return context

@login_required
def selectinterest(request):

    interestselected = False
    if request.method == 'POST':
        interest_select_form = forms.interestSelectForm(data=request.POST,instance=request.user)
        # ChoiceField.clean(forms.userGenderForm(),gender_form)
        # print(cleaned_gender_form)
        if interest_select_form.is_valid():
            user=interest_select_form.save(commit=False)
            interests = request.POST.getlist('interests')
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



@login_required
def selectprofilepicture(request):
    profilepictureselected = False
    profile=request.user.userprofile.user

    if request.method == 'POST':
        profile_pic_select_form = forms.profilePicSelectForm(data=request.POST,instance=request.user)
        # ChoiceField.clean(forms.userGenderForm(),gender_form)
        # print(cleaned_gender_form)
        if profile_pic_select_form.is_valid():
            user_pic = profile_pic_select_form.save(commit=False)

            if 'profile_pic' in request.FILES:
                print('found it')
                print(user_pic)
                print(request.FILES)
                # print(user_pic.userprofile.profile_pic)
                # If yes, then grab it from the POST form reply
                user_pic.userprofile.profile_pic = request.FILES['profile_pic']

            # Now save model
            user_pic.userprofile.save()

            profilepictureselected = True

            return HttpResponseRedirect(reverse_lazy("posts:post_list"))
        else:
            print(profile_pic_select_form.errors)
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
        profile_pic_select_form = forms.profilePicSelectForm()
    return render(request,'accounts/choose_profile_pic_page.html',{'form':profile_pic_select_form,'profilepictureselected':profilepictureselected})
