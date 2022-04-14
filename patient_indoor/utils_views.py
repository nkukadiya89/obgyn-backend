from .models import IndoorAdviceModel
from .serializers import IndoorAdviceSerializers


def indoor_advice_insert(advice_json,patient_indoor_id, created_by):

    IndoorAdviceModel.objects.filter(patient_indoor_id=patient_indoor_id).delete()

    
    for advice in advice_json:
        advice["patient_indoor"] = patient_indoor_id
        advice["created_by"] = created_by
        indoor_advice = IndoorAdviceModel()
        serializer = IndoorAdviceSerializers(indoor_advice, data=advice)

        if serializer.is_valid():
            serializer.save()
