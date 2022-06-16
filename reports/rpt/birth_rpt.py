from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient.models import PatientModel
from patient_delivery.models import PatientDeliveryModel

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def birth_rpt(request, id, language_id=None):
    # patient = PatientModel.objects.filter(pk=id).first()
    patient_delivery = PatientDeliveryModel.objects.filter(pk=id, deleted=0).first()
    patient = patient_delivery.patient
    
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1,deleted=0).first()
    context = {}

    context["mother_name"] = "".join(
        [patient.first_name, " ", patient.middle_name, " ", patient.last_name])
    context["father_name"] = patient_delivery.husband_name
    context["address"] = "".join([" ", patient.city.city_name, " ",
                                  patient.district.district_name, " ",
                                  patient.taluka.taluka_name, " ", patient.state.state_name])
    context["age"] = patient.age
    context["date"] = patient_delivery.birth_date
    context["time"] = patient_delivery.birth_time
    context["gender"] = patient_delivery.child_gender
    context["weight"] = patient_delivery.weight
    context["child_status"] = patient_delivery.baby_status
    context["child_count"] = patient_delivery.live_male_female
    context["episitomy_by"] = patient_delivery.weight

    template_name = "reports/en/birth_report.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
