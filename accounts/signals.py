from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # get_or_create e idempotente: evita IntegrityError se o usuario ja
        # tiver perfil (loaddata, criacao manual, reexecucao do signal).
        Profile.objects.get_or_create(user=instance)
