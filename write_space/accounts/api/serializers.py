from django.db.models import Q

from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import userProfile

User = get_user_model()

class userDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
        "username"
        ]

class userCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label="Email Address")
    email2 = serializers.EmailField(label="Confirm Email")
    class Meta:
        model = User
        fields = [
        "username",
        "password",
        "email",
        "email2",
        ]

        extra_kwargs = {"password":{"write_only":True}}

    def validate_email2(self,value):
        data = self.get_initial()
        email = data.get("email")
        email2 = value
        if email != email2:
            raise serializers.ValidationError("emails doesn't match")

        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError("a user with that email already exists")

        return value

    def create(self,validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        user = User(username = username,email = email)
        user.set_password(password)
        user.save()
        userProfile.objects.create(user=user)
        return validated_data


class userLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank = True,read_only = True)
    username = serializers.CharField(allow_blank = True,required = False)
    email = serializers.EmailField(label="Email Address",allow_blank = True,required = False)
    class Meta:
        model = User
        fields = [
        "email",
        "username",
        "password",
        "token",
        ]

        extra_kwargs = {"password":{"write_only":True}}

    def validate(self,data):
        user_obj = None
        email = data.get("email")
        username = data.get("username")
        password = data["password"]
        if not email and not username:
            raise serializers.ValidationError("a username or an email address is required")

        user = User.objects.filter(Q(email=email)|Q(username=username)).distinct()
        user = user.exclude(email__isnull=True).exclude(email__exact="")
        print(user)
        print(user.count)

        if user.exists:
            user_obj = user.first
        else:
            raise serializers.ValidationError("this username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("incorrect password. please check and try again")
        data["token"] = "some random token"

        return data
