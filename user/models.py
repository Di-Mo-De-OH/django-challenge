from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self,email,password,*args,**kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active  = True
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,*args, **kwargs):
        user = self.create_user(email,password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    name =models.CharField(max_length=100)
    email = models.EmailField(unique = True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects= UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name ="user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.name

    @property
    def username(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True