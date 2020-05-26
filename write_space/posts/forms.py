from django import forms
from posts.models import Post, Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class PostForm(forms.ModelForm):

    class Meta():
        # main_image=forms.HiddenInput()
        model=Post
        fields=("title","post_heading","text","cartegory")
        widgets={
        "title":forms.TextInput(attrs={"class":"form-control","placeholder":"title of your post"}),
        "post_heading":forms.TextInput(attrs={"class":"form-control","placeholder":"provide any suitable heading for your post"}),
        'text': SummernoteWidget()
        }

# "text":forms.Textarea(attrs={"class":"form-control","placeholder":"Create your post here"}),

class imageForm(forms.ModelForm):
    class Meta():
        model=Post
        fields = ("main_image",)

class CommentForm(forms.ModelForm):

    class Meta():
        model=Comment
        fields=("text",)

        widgets={
        "text":forms.Textarea(attrs={"class":"form-control"}),
        }
