from user.models import User
from django.db.models.query import Q

def generate_patient_user_code(patient_user):
    seq_no = 0
    last_user = User.objects.filter(user_type=patient_user.user_type).filter(~Q(pk=patient_user.id)).last()
    if last_user:
        seq_no = int(last_user.user_code[-4:])
        seq_no += 1

    patient_user.user_code = patient_user.user_type[0] + '{:05}'.format(seq_no)
    patient_user.save()
