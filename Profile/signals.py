from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,*args, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
