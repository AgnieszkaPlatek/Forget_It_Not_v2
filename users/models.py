from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


#TODO Should I get rid of this custom User?
#TODO Fix this save method and remove signals

class User(AbstractUser):
        pass
    # def save(self, *args, **kwargs):
    #     super(User, self).save(*args, **kwargs)
    #     Token.objects.create(user=self)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
