from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from patient_delivery.models import PatientDeliveryModel
from patient_opd.models import PatientOpdModel


@csrf_exempt
def child_birth_rpt(request, id, language_id=None):
    # patient = PatientModel.objects.filter(pk=id).first()
    patient_delivery = PatientDeliveryModel.objects.filter(pk=id, deleted=0).first()

    if not patient_delivery:
        context = {}
        context["msg"] = False
        context["error"] = "Patient Delivery not found."
        return JsonResponse(context)

    patient = patient_delivery.patient

    patient_opd = (
        PatientOpdModel.objects.filter(patient=patient).order_by("-created_by").first()
    )

    patient = patient_delivery.patient

    if not patient:
        context = {}
        context["msg"] = False
        context["error"] = "Patient not found."
        return JsonResponse(context)

    context = {}
    context["mother_name"] = "".join(
        [
            patient_delivery.mother_name if patient_delivery.mother_name else " ",
            " ",
            patient_delivery.husband_name if patient_delivery.husband_name else " ",
            " ",
            # patient.middle_name if patient.middle_name else " ",
            # " ",
            patient_delivery.delivery_last_name
            if patient_delivery.delivery_last_name
            else " ",
        ]
    )
    context["father_name"] = "".join(
        [
            patient_delivery.husband_name if patient_delivery.husband_name else " ",
            " ",
            patient_delivery.delivery_husband_father_name
            if patient_delivery.delivery_husband_father_name
            else " ",
            " ",
            patient_delivery.delivery_last_name
            if patient_delivery.delivery_last_name
            else " ",
        ]
    )

    # context["father_name"] = patient_delivery.husband_name if patient_delivery.husband_name else " "
    context["mother_address"] = "".join(
        [
            " ",
            patient_delivery.city if patient_delivery.city else " ",
            " ",
            patient_delivery.taluka if patient_delivery.taluka else " ",
            " ",
            patient_delivery.district if patient_delivery.district else " ",
            " ",
            patient_delivery.state if patient_delivery.state else " ",
        ]
    )
    context["mother_city"] = patient_delivery.city if patient_delivery.city else " "
    context["mother_taluka"] = (
        patient_delivery.taluka if patient_delivery.taluka else " "
    )
    context["mother_district"] = (
        patient_delivery.district if patient_delivery.district else " "
    )
    context["address"] = " ".join(
        [
            " ",
            patient_delivery.city if patient_delivery.city else " ",
            " ",
            patient_delivery.taluka if patient_delivery.taluka else " ",
            " ",
            patient_delivery.district if patient_delivery.district else " ",
            " ",
            patient_delivery.state if patient_delivery.state else " ",
        ]
    )
    context["district"] = (
        patient_opd.consulted_by.hospital.district.district_name
        if patient_opd.consulted_by.hospital.district.district_name
        else " "
    )
    context["taluka"] = (
        patient_opd.consulted_by.hospital.taluka.taluka_name
        if patient_opd.consulted_by.hospital.taluka.taluka_name
        else " "
    )
    context["city"] = (
        patient_opd.consulted_by.hospital.city
        if patient_opd.consulted_by.hospital.city
        else " "
    )
    context["pin"] = patient_delivery.pin

    context["regd_no"] = patient_delivery.regd_no
    context["age"] = patient.age
    context["date"] = patient_delivery.birth_date
    context["time"] = patient_delivery.birth_time
    context["gender"] = patient_delivery.child_gender
    context["weight"] = patient_delivery.weight
    context["child_name"] = patient_delivery.child_name
    context["child_status"] = patient_delivery.baby_status
    context["child_count"] = patient_delivery.live_male_female
    context["episitomy_by"] = patient_delivery.weight
    context["hospital_name"] = patient_opd.consulted_by.hospital.hospital_name
    context["hospital_address"] = "".join(
        [
            " ",
            patient_opd.consulted_by.hospital.city
            if patient_opd.consulted_by.hospital.city
            else " ",
            " ",
            patient_opd.consulted_by.hospital.district.district_name
            if patient_opd.consulted_by.hospital.district.district_name
            else " ",
            " ",
            patient_opd.consulted_by.hospital.taluka.taluka_name
            if patient_opd.consulted_by.hospital.taluka.taluka_name
            else " ",
            " ",
            patient_opd.consulted_by.hospital.state.state_name
            if patient_opd.consulted_by.hospital.state.state_name
            else " ",
        ]
    )
    context["religion"] = patient_delivery.religion.field_value
    context["father_education"] = (
        patient_delivery.father_education.field_value
        if patient_delivery.father_education
        else ""
    )
    context["mother_education"] = patient_delivery.mother_education.field_value
    context["father_occupation"] = patient_delivery.father_occupation.field_value
    context["mother_occupation"] = patient_delivery.mother_occupation.field_value
    context["marriage_age"] = patient_delivery.marriage_age
    context["live_male_female"] = patient_delivery.live_male_female
    context["delivery_type"] = patient_delivery.delivery_type
    context["pregnancy_weeks"] = patient_delivery.weeks
    context["mobile"] = patient.phone

    template_name = "reports/en/child_birth.html"
    return render(
        request,
        template_name,
        {
            "context": context,
        },
    )
