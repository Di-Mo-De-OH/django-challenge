from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id","nickname","email","password","is_superuser","is_staff")

    def create(self,validated_data):
        password = validated_data.pop("password",None)
        if password is None:
            raise ValueError("password is required")
        user = UserModel.objects.create_user(password = password,**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("id","nickname","email","password","profile_image")
        read_only_fields = ("id","email")

    def update(self,instance,validated_data):
        instance.nickname = validated_data.get("nickname",instance.nickname)
        password = validated_data.get("password",instance.password)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self,attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(request=self.context.get("request"),**attrs)
            if not user:
                raise serializers.ValidationError(
                    detail="로그인 할 수 없음",code = "authenticate"
                )
        else:
            raise serializers.ValidationError(
                detail="이메일과 비밀번호는 필수합니다.",code = "authenticate"
            )
        attrs["user"] = user
        return attrs







