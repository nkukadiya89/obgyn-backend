from diagnosis.models import DiagnosisModel
from diagnosis.serializers import DiagnosisSerializers
from patient_prescription.models import PatientPrescriptionModel
from diagnosis.models import DiagnosisMedicineModel


def link_diagnosis(request, medicine_id):

    diagnosis_type = request.data.get('diagnosis_type', "D")
    if diagnosis_type.upper() == "D":
        diagnosis = DiagnosisModel.objects.filter(
            deleted=0, created_by=request.data.get('created_by'), diagnosis_name__iexact=request.data.get('diagnosis_name'), diagnosis_type="D").first()
    elif diagnosis_type.upper() == "U":
        diagnosis = DiagnosisModel.objects.filter(
            deleted=0, created_by=request.data.get('created_by'), fu=request.data.get('fu'), ut_weeks=request.data.get('ut_weeks'), diagnosis_type="U").first()

    if diagnosis == None:
        diagnosis = DiagnosisModel()
        diagnosis_dict = {}
        if diagnosis_type == "D":
            diagnosis_dict["diagnosis_type"] = "D"
            diagnosis_dict["diagnosis_name"] = request.data.get(
                'diagnosis_name', "")
        else:
            diagnosis_dict["diagnosis_type"] = "U"
            diagnosis_dict["fu"] = request.data.get('fu')
            diagnosis_dict["ut_weeks"] = request.data.get('ut_weeks')

        diagnosis_dict["medicine"] = [medicine_id]
        diagnosis_dict["created_by"] = request.data.get('created_by')
        diagnosis_dict["deleted"] = 0

        serializer = DiagnosisSerializers(diagnosis, data=diagnosis_dict)
        if serializer.is_valid():
            serializer.save()

    diagnosis = DiagnosisModel.objects.get(
            pk=serializer.data["diagnosis_id"])

    diagnosis.medicine.add(medicine_id)
    diagnosis.save()
    return True



def delete_child_table(medicine_list):
    patient_prescription = PatientPrescriptionModel.objects.filter(medicine_id__in=medicine_list)
    if len(patient_prescription)>0:
        patient_prescription.update(medicine=None)
        # patient_prescription.save()

    DiagnosisMedicineModel.objects.filter(medicinemodel__medicine_id__in=medicine_list).delete()
