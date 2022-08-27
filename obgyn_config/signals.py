from obgyn_config.models import ObgynConfigModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save,sender=ObgynConfigModel)
def update_user_from_obgyn_config(sender,**kwargs):
    user = kwargs.get('instance').user
    user.state = kwargs.get('instance').state
    user.district = kwargs.get('instance').district
    user.taluka = kwargs.get('instance').taluka
    user.city = kwargs.get('instance').city
    user.save()
