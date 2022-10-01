from obgyn_config.models import ObgynConfigModel
from django.contrib.auth.models import Group


def create_profile(user):
    if user.user_type in ["HOSPITAL", "DOCTOR"]:
        ObgynConfigModel.objects.create(user=user, state=user.state,city=user.city,taluka=user.taluka,district=user.district)

    group = Group.objects.filter(name__iexact=user.user_type).first()
    if group:
        group.user_set.add(user)
        group.save()
