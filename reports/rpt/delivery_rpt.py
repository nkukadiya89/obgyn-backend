from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient.models import PatientModel
from patient_delivery.models import PatientDeliveryModel
from user.models import User

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delivery_rpt(request, start_date=None, end_date=None,id_list=None, language_id=1):
    
    patient_delivery_list = PatientDeliveryModel.objects.filter(created_by=request.user.id, deleted=0)
    
    if len(id_list)>0:
        id_list = id_list.split(",")
        patient_delivery_list = patient_delivery_list.filter(patient_delivery_id__in=id_list)
    if start_date and not end_date:
        patient_delivery_list = patient_delivery_list.filter(created_at__date=start_date)
    elif start_date and end_date:
        patient_delivery_list = patient_delivery_list.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

    context_list=[]
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1,deleted=0).first()

    if not template_header:
        raise "Template not found"
        
    for patient_delivery in patient_delivery_list:
        patient = patient_delivery.patient
        
        context = {}

        context["regd_no"] = patient_delivery.regd_no
        context["birth_date"] = patient_delivery.birth_date
        context["birth_time"] = patient_delivery.birth_time
        context["gender"] = patient_delivery.child_gender
        hospital_name = User.objects.filter(pk=request.user.id).first()#.hospital.hospital_name

        context["birth_place"] = hospital_name.hospital.hospital_name

        context["mother_name"] = "".join(
            [patient.first_name, " ", patient.middle_name, " ", patient.last_name])
        context["father_name"] = patient_delivery.husband_name
        context["address"] = "".join([" ", patient.city.city_name, " ",
                                    patient.district.district_name, " ",
                                    patient.taluka.taluka_name, " ", patient.state.state_name])
        context["mobile"] = patient_delivery.patient.phone
        context["nationality"] = "Indian"
        context["religion"] = patient_delivery.religion
        context["age"] = patient.age
        context["child_count"] = int(patient_delivery.no_of_delivery) + 1
        context["weight"] = patient_delivery.weight
        context["child_count"] = int(patient_delivery.live_male_female)
        context["mother_education"] = patient_delivery.mother_education
        context["father_education"] = patient_delivery.father_education
        context["mother_occupation"] = patient_delivery.mother_occupation
        context["father_occupation"] = patient_delivery.father_occupation

        context["child_status"] = patient_delivery.baby_status
        context_list.append(context)

    template_name = "reports/en/delivery_report.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})
