from obgyn_config.models import ObgynConfigModel


def create_profile(user):
    if user.user_type in ["HOSPITAL", "DOCTOR"]:
        ObgynConfigModel.objects.create(
            user=user
        )
