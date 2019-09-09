from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import userProfile
from posts.models import Cartegory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
GENDER = (
    ('', '-------'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'Prefer not to say')
    )

class signupForm(forms.ModelForm):

    class Meta:
        fields=("first_name","last_name","username","email","password")
        model=get_user_model()
        widgets={
        "first_name":forms.TextInput(attrs={"class":"form-control","placeholder":"input your firstname"}),
        "last_name":forms.TextInput(attrs={"class":"form-control","placeholder":"input your lastname"}),
        "username":forms.TextInput(attrs={"class":"form-control","placeholder":"choose a username"}),
        "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"input your email address"}),
        "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"choose a password"}),
        }


        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.helper = FormHelper()
        #     self.helper.layout = Layout(
        #         Row(
        #             Column('first_name', css_class='form-group col-lg-6 col-md-6 col-sm-6'),
        #             Column('last_name', css_class='form-group col-lg-6 col-md-6 col-sm-6'),
        #             css_class='row'
        #         ),
        #         'username',
        #         'email',
        #         'password',
        #         Submit('submit', 'Sign in')
        #     )

class userGenderForm(forms.ModelForm):
    gender=forms.ChoiceField(choices=GENDER,widget=forms.RadioSelect)
    class Meta():
        fields = ("gender",)
        model = userProfile

        # widgets={
        # "gender":forms.TextInput(attrs={"class":"form-control"}),
        # }

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.helper = FormHelper()
        #     self.helper.layout = Layout(
        #         'gender',
        #         Submit('submit', 'Sign in')
        #     )


class  LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs = {"class":"form-control","placeholder":"input your registered username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs = {"class":"form-control","placeholder":"input your password"}))


class interestSelectForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
    queryset = Cartegory.objects.all(),
    widget = forms.CheckboxSelectMultiple,
    )
    class Meta():
        model=userProfile
        fields=("interests",)



class profilePicSelectForm(forms.ModelForm):
    class Meta():
        model=userProfile
        fields=("profile_pic","background_pic")

class bioForm(forms.ModelForm):
    class Meta:
        fields=("bio",)
        model=userProfile
        widgets={
        "bio":forms.Textarea(attrs={"class":"form-control","placeholder":"Tell us your story"}),
        }
