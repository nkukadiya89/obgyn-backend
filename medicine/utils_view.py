from diagnosis.models import DiagnosisModel


def link_diagnosis(diagnosis_id, medicine_id):
    diagnosis = DiagnosisModel.objects.filter(pk=diagnosis_id).first()
    if diagnosis == None:
        return False

    diagnosis.medicine.add(medicine_id)
    diagnosis.save()
    return True
