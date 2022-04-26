from patient_usgform.models import USGFormChildModel
from patient_usgform.serializers import USGFormChildSerializers


def insert_child_usgform(request, patient_usgform_id):
    if "usg_child" in request.data:
        child_list = request.data.get('usg_child')

        if len(child_list)>0:
            USGFormChildModel.objects.filter(patient_usgform_id=patient_usgform_id).delete()

        child_dict = {}
        for child in child_list:
            child_dict["child_gender"] = child["child_gender"]
            child_dict["child_year"] = child["child_year"]
            child_dict["child_month"] = child["child_month"]
            child_dict["patient_usgform"] = patient_usgform_id
            child_dict["created_by"] = request.data.get('created_by')

            usgchild = USGFormChildModel()
            serializer = USGFormChildSerializers(usgchild, data=child_dict)

            if serializer.is_valid():
                serializer.save()
