from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email




class Profile(models.Model):
    nickName = models.CharField(max_length=20)

    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )

    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    point = models.IntegerField(default=0)
    twitter_name = models.CharField(max_length=100,blank=True, null=True)
    github_name = models.CharField(max_length=100,blank=True, null=True)


    def __str__(self):
        return self.nickName



class Study(models.Model):
    userStudy = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userStudy',
        on_delete=models.CASCADE
    )

    study_time = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    comment = models.TextField()
    language = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

