from consultation.models import ConsultationModel
from patient_billing.models import PatientBillingModel
from patient_discharge.models import PatientDischargeModel
from patient_indoor.models import PatientIndoorModel
from patient_usgform.models import PatientUSGFormModel

def delete_child_record(diagnosis_list):
    for diagnosis in diagnosis_list:
        consultation = ConsultationModel.objects.filter(diagnosis=diagnosis)
        print("consultation",consultation)
        if len(consultation)>0:
            consultation.update(diagnosis_id=None)

        patient_billing = PatientBillingModel.objects.filter(diagnosis=diagnosis)
        if len(patient_billing)>0:
            print(patient_billing)
            patient_billing.update(diagnosis_id=None)

        patient_discharge = PatientDischargeModel.objects.filter(diagnosis=diagnosis)
        if len(patient_discharge)>0:
            print(patient_discharge)
            patient_discharge.update(diagnosis_id=None)

        patient_indoor = PatientIndoorModel.objects.filter(diagnosis=diagnosis)
        if len(patient_indoor)>0:
            print(patient_indoor)
            patient_indoor.update(diagnosis_id=None)

        patient_usgform = PatientUSGFormModel.objects.filter(diagnosis=diagnosis)
        if len(patient_usgform)>0:
            print(patient_usgform)
            patient_usgform.update(diagnosis_id=None)
