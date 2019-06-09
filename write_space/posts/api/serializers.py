from rest_framework import serializers
from accounts.api.serializers import userDetailSerializer
from rest_framework.fields import CurrentUserDefault
from posts.models import Post,Comment


class postListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
    view_name="posts_api:post_detail",
    lookup_field="pk",
    )
    class Meta:
        model = Post
        fields =[
        "url",
        "title",
        ]

class postDetailSerializer(serializers.ModelSerializer):
    # delete_url = serializers.HyperlinkedIdentityField(
    # view_name="posts_api:delete_post",
    # lookup_field=["username","pk"],
    # )
    comments_url = serializers.HyperlinkedIdentityField(
    view_name="posts_api:comments",
    lookup_field="pk",
    )
    add_comment_url = serializers.HyperlinkedIdentityField(
    view_name="posts_api:add_comment",
    )
    author = userDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields =[
        "pk",
        "author",
        "title",
        "post_heading",
        "main_image",
        "text",
        "clap",
        "viewed",
        # "delete_url",
        "created_at",
        "publish_date",
        "comments_url",
        "add_comment_url",
        ]


class postCommentsSerializer(serializers.ModelSerializer):
    edit_url = serializers.HyperlinkedIdentityField(
    view_name="posts_api:edit_comment",
    lookup_field = "pk",
    )

    author = userDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
        "pk",
        "author",
        "text",
        "created_at",
        "edit_url",

        ]

class addCommentSerializer(serializers.ModelSerializer):
    author = userDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
        "author",
        "text",
        ]

class editCommentSerializer(serializers.ModelSerializer):
    author = userDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
        "author",
        "text",
        ]

class postCreateSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    author = userDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
        "author",
        "title",
        "post_heading",
        "main_image",
        "text",
        "publish_date",
        ]

    # def save(self):
    #     author = CurrentUserDefault()  # <= magic!
    #     title = self.validated_data['title']
    #     post_heading = self.validated_data['post_heading']
    #     text = self.validated_data['text']
    #     main_image = self.validated_data['main_image']
    #     publish_date = self.validated_data['publish_date']
