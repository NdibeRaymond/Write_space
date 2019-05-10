from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views import generic
from posts import models
from posts.rec_engine import recEngine
from accounts.models import userProfile
from posts.forms import PostForm,CommentForm
# Create your views here.


class postListView(generic.ListView):
    # login_url="/login/"
    model=models.Post
    context_object_name="all_posts"
    template_name="posts/posts_list.html"

    def get_queryset(self):
         return models.Post.objects.filter(publish_date__lte=timezone.now()).order_by("-publish_date")


    def get_context_data(self,**kwargs):
        most_popular = recEngine.most_popular(self.request)
        context = super(postListView,self).get_context_data(**kwargs)
        context["most_popular_0"] = most_popular[0]
        context["most_popular_1"] = most_popular[1]
        context["most_popular_2"] = most_popular[2]
        context["most_popular_3"] = most_popular[3]
        context["most_popular_4"] = most_popular[4]
        return context



class PostDetailView(generic.DetailView):
    template_name="posts/post_detail.html"
    # context_object_name="post"
    model=models.Post

    def get_context_data(self,**kwargs):
        try:
            models.Post.objects.get(pk=self.kwargs.get("pk")).viewed.add(self.request.user)
        except:
            pass

        recommendation_from_history=recEngine.rec_from_history(self.request)
        recommendation_from_follow = recEngine.mvpu_follow(self.request)
        recommedation_from_user_interests = recEngine.rec_from_cat(self.request)

        context = super(PostDetailView,self).get_context_data(**kwargs)
        context["rec_history"] = recommendation_from_history
        context["rec_follow"] = recommendation_from_follow
        context["rec_interest"] = recommedation_from_user_interests
        return context




class userPostDetailView(LoginRequiredMixin,generic.DetailView):
    login_url="/accounts/login/"
    # context_object_name="post"
    template_name="posts/user_post_detail.html"
    model=models.Post
    def get_context_data(self,**kwargs):
        models.Post.objects.get(pk=self.kwargs.get("pk")).viewed.add(self.request.user)

        recommendation_from_history=recEngine.rec_from_history(self.request)
        recommendation_from_follow = recEngine.mvpu_follow(self.request)
        recommedation_from_user_interests = recEngine.rec_from_cat(self.request)

        context = super(userPostDetailView,self).get_context_data(**kwargs)
        context["rec_history"] = recommendation_from_history
        context["rec_follow"] = recommendation_from_follow
        context["rec_interest"] = recommedation_from_user_interests
        return context

class userPostListView(LoginRequiredMixin,generic.ListView):
    login_url="/accounts/login/"
    template_name="posts/user_post_list.html"
    context_object_name="user_post"
    # redirect_field_name="posts/user_post_list.html"
    model=models.Post

    def get_queryset(self):
        return models.Post.objects.filter(author__exact=get_user_model().objects.get(username__exact=self.kwargs.get("username"))).order_by("-created_at")

    def get_context_data(self,**kwargs):
        user = get_user_model().objects.get(username__exact=self.kwargs.get("username"))
        context = super(userPostListView,self).get_context_data(**kwargs)
        context["user"] = user

        return context


# class myDraftDetailView(generic.DetailView):
#     # context_object_name="post"
#     model=models.Post

# class myDraftListView(LoginRequiredMixin,generic.ListView):
#     login_url="/login/"
#     template_name="posts/post_draft_list.html"
#     context_object_name="all_drafts"
#     redirect_field_name="posts/post_draft_list.html"
#     model=models.Post
#
#     def get_queryset(self):
#         return Post.objects.filter(publish_date__isnull=True,author__exact=get_user_model().get(username__exact=request.user.username)).order_by("created_at")


class CreatePostView(LoginRequiredMixin,generic.CreateView):
    login_url="/accounts/login/"
    redirect_field_name="posts/user_post_detail.html"
    # success_url=reverse("posts:user_post_detail",kwargs={"pk":request.POST.pk})


    form_class=PostForm
    model=models.Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(generic.UpdateView,LoginRequiredMixin):
    login_url="/accounts/login/"
    redirect_field_name="posts/user_post_detail.html"
    form_class=PostForm
    model=models.Post
    # success_url= reverse("posts:user_post_detail",kwargs={"pk":models.Post.pk})

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class PostDeleteView(generic.DeleteView,LoginRequiredMixin):
    # success_url=reverse_lazy("posts:user_post_list")
    # redirect_field_name = "posts/user_post_list.html"
    login_url="/accounts/login/"
    model=models.Post
    def get_success_url(self,**kwargs):
        return reverse_lazy("posts:user_post_list",kwargs={"username":self.kwargs.get("username")})


class postSaveView(LoginRequiredMixin,generic.DetailView):
    login_url="/accounts/login/"
    success_url = reverse_lazy("posts:post_detail")
    model=models.Post

    def get_context_data(self,**kwargs):

        author = models.Post.objects.get(pk=self.kwargs.get("pk")).author

        if author != self.request.user:
            user=userProfile.objects.get(user__exact=get_user_model().objects.get(username__exact=self.request.user.username))
            user.saved_for_future.add(models.Post.objects.get(pk=self.kwargs.get("pk")))

        context = super(postSaveView,self).get_context_data(**kwargs)
        return context

class savedListView(LoginRequiredMixin,generic.ListView):
    login_url="/accounts/login/"
    model = userProfile
    context_object_name = "saved_posts"
    template_name = "posts/view_saved.html"

    def get_queryset(self,**kwargs):
        user =userProfile.objects.get(user=get_user_model().objects.get(username=self.kwargs.get("username")))
        saved_posts = user.saved_for_future.all()
        return saved_posts


class postUnsaveView(LoginRequiredMixin,generic.DetailView):
    login_url="/accounts/login/"
    success_url = reverse_lazy("posts:post_detail")
    model=models.Post

    def get_context_data(self,**kwargs):

        author = models.Post.objects.get(pk=self.kwargs.get("pk")).author

        if author != self.request.user:
            user=userProfile.objects.get(user__exact=get_user_model().objects.get(username__exact=self.request.user.username))
            user.saved_for_future.remove(models.Post.objects.get(pk=self.kwargs.get("pk")))

        context = super(postUnsaveView,self).get_context_data(**kwargs)
        return context


class postClapView(LoginRequiredMixin,generic.DetailView):
    login_url="/accounts/login/"
    success_url = reverse_lazy("posts:post_detail")
    model=models.Post

    def get_context_data(self,**kwargs):
        models.Post.objects.get(pk=self.kwargs.get("pk")).clap.add(self.request.user)
        context = super(postClapView,self).get_context_data(**kwargs)
        return context





class cartegoryView(generic.ListView):
    template_name="posts/cartegory_page.html"
    # context_object_name="posts"
    # model=models.POST

    def get_queryset(self,**kwargs):
        if self.kwargs.get("name") == "All":
            self.current = models.Cartegory.objects.all()
            return self.current
        else:
            self.current = models.Cartegory.objects.get(name__exact=self.kwargs.get("name")).children.all()
            return self.current

    def get_context_data(self,**kwargs):
        posts = models.Post.objects.all()
        try:
            cartegory_posts=posts.filter(cartegory=models.Cartegory.objects.get(name__exact=self.kwargs.get("name")))
        except:
            cartegory_posts = []
        context = super(cartegoryView,self).get_context_data(**kwargs)
        print(self.current)
        context["current_cartegory"] = self.current
        context["current_cartegory_posts"] = cartegory_posts
        # for each in self.current.getlist:
        #     print(each.pk)
        #     print(each.name)
        #     print(self.request.user.userprofile.interests)
        #     print(each in self.request.user.userprofile.interests)
        #     print(each.name in self.request.user.userprofile.interests)

        return context










########################################################################
########################################################################

@login_required
def join_cartegory_view(request,**kwargs):
    userprofile=userProfile.objects.get(user__exact=request.user)
    cartegory = models.Cartegory.objects.get(pk=kwargs.get("pk"))
    if not cartegory in userprofile.interests.all():
        userprofile.interests.add(cartegory)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def leave_cartegory_view(request,**kwargs):
    userprofile=userProfile.objects.get(user__exact=request.user)
    cartegory = models.Cartegory.objects.get(pk=kwargs.get("pk"))
    if cartegory in userprofile.interests.all():
        userprofile.interests.remove(cartegory)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(models.Post,pk=pk)
    if request.method =="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            post_comment=form.save(commit=False)

            post_comment.author = request.user
            post_comment.text = request.POST["text"]
            post_comment.post  = post
            post_comment.save()

            return redirect("posts:post_detail",pk=post.pk)
    else:
        form=CommentForm()
        return render(request,"posts/comment_form.html",{"form":form})


@login_required
def post_publish(request,pk):
    post=get_object_or_404(models.Post, pk=pk)
    post.publish()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def post_unpublish(request,pk):
    post=get_object_or_404(models.Post, pk=pk)
    post.unpublish()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Create your views here.


# class postList(generic.ListView):
#     model = models.Post
#
#
# class UserPosts(generic.ListView):
#     model = models.Post
#     template_name = "posts/user_post_list.html"
#
#     def get_queryset(self):
#         try:
#             self.post_user = User.objects.prefetch_related("posts").get(username__iexact = self.kwargs.get("username"))
#         except User.DoesNotExist:
#             raise Http404
#         else:
#             return self.post_user.posts.all()
#
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_user"] = self.post_user
#         return context
#
#
# class PostDetail(generic.DetailView):
#     model = models.Post
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user__username__iexact = self.kwargs.get("username"))
#
#
# class CreatePost(LoginRequiredMixin,generic.CreateView):
#     fields = ("message","group")
#     model = models.Post
#
#     def form_valid(self,form):
#         self.object = form.save(commit = False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)
#
# class DeletePost(LoginRequiredMixin,generic.DeleteView):
#     model = models.Post
#     success_url = reverse_lazy("posts:all")
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user_id = self.request.user.id)
#
#     def delete(self,*args,**kwargs):
#         messages.success(self.request,"Post Deleted")
#         return super().delete(*args,**kwargs)
