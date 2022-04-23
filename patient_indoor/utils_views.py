from .models import IndoorAdviceModel
from .serializers import IndoorAdviceSerializers


# def indoor_advice_insert(advice_json,patient_indoor_id, created_by):
def indoor_advice_insert(request,patient_indoor_id):

    advice_list = request.data.get("advice_lst")

    if len(advice_list)>0:
        IndoorAdviceModel.objects.filter(patient_indoor_id=patient_indoor_id).delete()


    advice_dict = {}
    for advice in advice_list:
        advice_dict["patient_indoor"] = str(patient_indoor_id)
        advice_dict["advice"] = advice
        advice_dict["created_by"] = request.data.get("created_by")
        indoor_advice = IndoorAdviceModel()
        serializer = IndoorAdviceSerializers(indoor_advice, data=advice_dict)

        if serializer.is_valid():
            serializer.save()
