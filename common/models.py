import os.path

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser

class myUser(AbstractUser):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    photo = models.ImageField(blank=True,upload_to='photo/',null=True)
    nickname = models.TextField(unique=True, max_length=60)

    def delete(self, *args,**kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT ,self.photo.name))
        super(Profile,self).delete(*args,**kargs)

    def photoname(self):
        return self.photo.name.split('/')[-1]



# Create your models here.
