from advice.models import AdviceGroupModel
from patient_indoor.models import IndoorAdviceModel



def insert_advice_group(request,advice_id):
    advice_group_name = str(request.data.get('advice_group_name')).strip()
    advice_group = AdviceGroupModel.objects.filter(advice_group=advice_group_name).first()
    if advice_group == None:
        advice_group = AdviceGroupModel.objects.create(advice_group=advice_group_name,
                                                        created_by=request.data.get('created_by'),
                                                        deleted=0)

    advice_group.advice.add(advice_id)



def delete_child_records(advice_list):
    for advice in advice_list:
        indoor_advice = IndoorAdviceModel.objects.filter(advice=advice)
        # print(indoor_advice.indoor_advice_id)
        indoor_advice.delete()