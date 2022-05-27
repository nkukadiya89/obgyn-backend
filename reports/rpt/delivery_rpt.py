from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient.models import PatientModel
from patient_delivery.models import PatientDeliveryModel
from user.models import User

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delivery_report(request, start_date, end_date, language_id):
    # patient = PatientModel.objects.filter(pk=id).first()
    patient_delivery = PatientDeliveryModel.objects.filter(pk=id).first()
    patient = patient_delivery.patient
    
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()
    context = {}

    context["regd_no"] = patient_delivery.regd_no
    context["birth_date"] = patient_delivery.birth_date
    context["birth_time"] = patient_delivery.birth_time
    context["gender"] = patient_delivery.child_gender
    doctor_id = patient_delivery.created_by
    hospital_name = User.objects.filter(pk=doctor_id).first().hospital.hospital_name

    context["birth_place"] = hospital_name

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
    context["father_occupation"] = patient_delivery.father_occupation

    context["child_status"] = patient_delivery.baby_status
    context["child_count"] = patient_delivery.live_male_female
    context["episitomy_by"] = patient_delivery.weight

    template_name = "reports/en/delivery_report.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
