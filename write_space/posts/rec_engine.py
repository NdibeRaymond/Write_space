from django.contrib.auth import get_user_model
from django.utils import timezone
from . import models
from accounts import models
import statistics
from collections import Counter
import random
# from django.http import request


#########################################
##This is the recommendation Engine. The class that helps recommendation
##posts based on the categories you like, the most viewed posts by the people you follow,
##your post viewing history, and the most viewed posts of allow
#######################################
class recEngine():

    def get_queryset(request=None,query=None):
        users = get_user_model().objects.all()
        try:
            user = get_user_model().objects.get(username__exact=request.user.username)
        except:
            user = None
        all_posts = models.Post.objects.all().filter(publish_date__lte=timezone.now())
        all_cartegories = models.Cartegory.objects.all()

        if query == "users":
            return users
        elif query == "user":
            return user
        elif query == "all_posts":
            return all_posts
        elif query == "all_cartegories":
            return all_cartegories


##################################################
##This function returns five most popular posts
###############################################
    def most_popular(request):
        all_cartegories = recEngine.get_queryset(request,query = "all_cartegories")
        all_posts = recEngine.get_queryset(request,query = "all_posts")
        cat_posts = []
        for each_cat in all_cartegories:
            cat_posts.append(all_posts.filter(cartegory=each_cat))

        posts_view_dict_list = []
        for each_post_list in cat_posts:
            posts_view_dict = {}
            for each_post in each_post_list:
                posts_view_dict[each_post] = each_post.viewed.count()
            if posts_view_dict:
                posts_view_dict_list.append(posts_view_dict)

        posts_with_most_view = []
        for each_dict in posts_view_dict_list:
            count = 0
            post_obj = None
            for each in each_dict:
                if each_dict[each] > count:
                    count = each_dict[each]
                    post_obj = each
            if post_obj != None:
                posts_with_most_view.append(post_obj)
        try:
            random.shuffle(posts_with_most_view)
        except:
            pass
        return posts_with_most_view





######################################################
##This function returns 1 most viewed post among people you follow
#####################################################
    def mvpu_follow(request):
        users = recEngine.get_queryset(request,query = "users")
        user = recEngine.get_queryset(request,query = "user")
        all_posts = recEngine.get_queryset(request,query = "all_posts")
        try:
            following=users.filter(userprofile__follower=user.userprofile)
        except:
            following=[]
        users_views=[]
        most_viewed=[]
        for each_user in following:
            users_views.append(all_posts.filter(viewed=each_user))

        for each_view_dict in users_views:
            for each_post in each_view_dict:
                most_viewed.append(each_post)
        most_common_two = Counter(most_viewed).most_common(2)
        try:
            random_num = random.randint(0,len(most_common_two)-1)
        except:
            random_num = 0
        try:
            most_viewed = most_common_two[random_num][0]
        except:
            most_viewed = []
        return most_viewed




#######################################################
##This function returns one post based on the most
##viewed cartegory in your viewing history
#######################################################
    def rec_from_history(request):
        users = recEngine.get_queryset(request,query = "users")
        user = recEngine.get_queryset(request,query = "user")
        all_posts = recEngine.get_queryset(request,query = "all_posts")
        posts_you_viewed = all_posts.filter(viewed=user)

        cartegory_of_posts = []
        for each_post in posts_you_viewed:
            cartegory_of_posts.append(each_post.cartegory)
        most_viewed_cats = Counter(cartegory_of_posts).most_common(2)
        random_num = random.randint(0,len(most_viewed_cats)-1)
        most_viewed_cat = most_viewed_cats[random_num][0]
        posts_of_cat = all_posts.filter(cartegory=most_viewed_cat)
        try:
            random_num = random.randint(0,len(posts_of_cat)-1)
        except:
            random_num = 0
        try:
            return posts_of_cat[random_num]
        except:
            posts_of_cat=[]
            return posts_of_cat




################################################
##This function returns one post based on the cartegories
##you follow
###############################################
    def rec_from_cat(request):
        user = recEngine.get_queryset(request,query = "user")
        all_posts = recEngine.get_queryset(request,query = "all_posts")
        try:
            your_cartegories = user.userprofile.interests.all()
        except:
            your_cartegories = []
        cat_posts = []
        for each_cat in your_cartegories:
            cat_posts.append(all_posts.filter(cartegory=each_cat))

        posts_view_dict_list = []
        for each_post_list in cat_posts:
            posts_view_dict = {}
            for each_post in each_post_list:
                posts_view_dict[each_post] = each_post.viewed.count()
            if posts_view_dict:
                posts_view_dict_list.append(posts_view_dict)

        posts_with_most_view = []
        for each_dict in posts_view_dict_list:
            count = 0
            post_obj = None
            for each in each_dict:
                if each_dict[each] > count:
                    count = each_dict[each]
                    post_obj = each
                elif each_dict[each] == count:
                        posts_with_most_view.append(each)
            if post_obj != None:
                posts_with_most_view.append(post_obj)
        try:
            random_num = random.randint(0,len(posts_with_most_view)-1)
        except:
            random_num = 0
        try:
            return posts_with_most_view[random_num]
        except:
            posts_with_most_view=[]
            return posts_with_most_view
