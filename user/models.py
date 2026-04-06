from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password,*args,**kwargs):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(email=self.normalize_email(email),*args,**kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,password,*args,**kwargs):
        user = self.create_user(email=self.normalize_email(email),password = password,*args,**kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class UserModel(AbstractBaseUser,PermissionsMixin):
    nickname = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to = "users/profile_images",default="users/blank_profile_image.png")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
