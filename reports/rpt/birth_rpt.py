from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from patient.models import PatientModel
from patient_delivery.models import PatientDeliveryModel
from template_header.models import TemplateHeaderModel


@csrf_exempt
def birth_rpt(request, id, language_id=None):
    # patient = PatientModel.objects.filter(pk=id).first()
    patient_delivery = PatientDeliveryModel.objects.filter(pk=id, deleted=0).first()

    if not patient_delivery:
        context = {}
        context["msg"] = False
        context["error"] = "Patient Delivery not found."
        return JsonResponse(context)

    patient = patient_delivery.patient

    if not patient:
        context = {}
        context["msg"] = False
        context["error"] = "Patient not found."
        return JsonResponse(context)

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(
            created_by=request.user.id, language_id=language_id, deleted=0
        ).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(
            created_by=request.user.id, deleted=0
        ).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    context = {}
    context["mother_name"] = "".join(
        [
            patient_delivery.mother_name if patient_delivery.mother_name else " ",
            " ",
            patient_delivery.delivery_last_name
            if patient_delivery.delivery_last_name
            else " ",
        ]
    )
    context["father_name"] = (
        patient_delivery.husband_name if patient_delivery.husband_name else " "
    )
    context["address"] = "".join(
        [
            " ",
            patient_delivery.city.city_name if patient_delivery.city.city_name else " ",
            " ",
            patient_delivery.taluka if patient_delivery.taluka else " ",
            " ",
            patient_delivery.district if patient_delivery.district else " ",
            " ",
            patient_delivery.state if patient_delivery.state else " ",
        ]
    )
    context["age"] = patient.age
    context["date"] = patient_delivery.birth_date
    context["time"] = patient_delivery.birth_time
    context["gender"] = patient_delivery.child_gender
    context["weight"] = patient_delivery.weight
    context["child_status"] = patient_delivery.baby_status
    context["child_count"] = patient_delivery.live_male_female
    context["episitomy_by"] = patient_delivery.weight

    template_name = "reports/en/birth_report.html"
    return render(
        request,
        template_name,
        {
            "context": context,
            "template_header": template_header.header_text.replace("'", '"'),
        },
    )
