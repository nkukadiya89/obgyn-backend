from patient_prescription.models import PatientPrescriptionModel
from patient_prescription.serializers import PatientPrescriptionSerializers


def add_medicine_for_consultaion(request, consultation_id):
    medicine_list = request.data.get('medicine')

    #delete already existing medicine against provided consultation_id
    if len(medicine_list) > 0:
        prescription = PatientPrescriptionModel.objects.filter(consultation_id=consultation_id)
        prescription.delete()
    

    prescription_data = {}
    for medicine in medicine_list:
        prescription = PatientPrescriptionModel()
        prescription_data["medicine"] = medicine
        prescription_data["consultation"] = consultation_id
        prescription_data["regd_no"] = request.data.get('regd_no')

        serializer = PatientPrescriptionSerializers(prescription, data=prescription_data)

        if serializer.is_valid():
            serializer.save()
