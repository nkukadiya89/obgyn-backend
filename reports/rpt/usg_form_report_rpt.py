from re import M
from django.shortcuts import render, HttpResponse

from rest_framework import status
from consultation.models import ConsultationModel
from patient_opd.models import PatientOpdModel
from patient_usgform.models import PatientUSGFormModel, USGFormChildModel
from template_header.models import TemplateHeaderModel
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from django.http import JsonResponse


@csrf_exempt
def usg_form_report_rpt(request, usg_form_id, language_id=None):
    usg_form = PatientUSGFormModel.objects.filter(pk=usg_form_id).first()
    if not usg_form:
        context = {}
        context["msg"] = False
        context["error"] = "Record Not found."
        return JsonResponse(context)

    patient_opd = usg_form.patient_opd

    if patient_opd == None:
        context = {}
        context["msg"] = False
        context["error"] = "OPD Does not exist."
        return JsonResponse(context)

    consultation = ConsultationModel.objects.filter(patient_opd=patient_opd).first()
    if consultation == None:
        context = {}
        context["msg"] = False
        context["error"] = "OPD Does not exist."
        return JsonResponse(context)

    context = {}
    context["doctor_name"] = "".join(
        [
            patient_opd.consulted_by.first_name if patient_opd.consulted_by.first_name else " ",
            " ",
            patient_opd.consulted_by.middle_name if patient_opd.consulted_by.middle_name else " ",
            " ",
            patient_opd.consulted_by.last_name if patient_opd.consulted_by.last_name else " ",
        ]
    )
    context["hospital_name"] = patient_opd.consulted_by.hospital.hospital_name
    context["hospital_address"] = "".join(
        [
            " ",
            patient_opd.consulted_by.hospital.city.city_name
            if patient_opd.consulted_by.hospital.city.city_name
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
    context["age"] = patient_opd.patient.age
    usgchild = {}
    usgchild["male"] = usgchild["female"] = ""
    m_cnt = f_cnt = 0
    usg_child_list = USGFormChildModel.objects.filter(
        patient_usgform=usg_form, deleted=0
    ).order_by("child_dob")
    for usg_child in usg_child_list:
        age_year = date.today().year - usg_child.child_dob.year
        age_month = date.today().month - usg_child.child_dob.month
        if usg_child.child_gender == "MALE":
            m_cnt = m_cnt + 1
            usgchild["male"] = (
                usgchild["male"] + "(" + str(m_cnt) + ") - " + str(age_year) + " y/s ,"
            )
        elif usg_child.child_gender == "FEMALE":
            f_cnt = f_cnt + 1
            usgchild["female"] = (
                usgchild["female"] + "(" + str(f_cnt) + ") - " + str(age_year)
            )

    context["child_detail"] = usgchild

    if consultation:
        context["hb"] = consultation.hb
        context["blood_group"] = consultation.blood_group
    else:
        context["hb"] = ""
        context["blood_group"] = ""

    context["name"] = "".join(
        [
            patient_opd.patient.first_name if patient_opd.patient.first_name else " ",
            " ",
            patient_opd.patient.middle_name if patient_opd.patient.middle_name else " ",
            " ",
            patient_opd.patient.last_name if patient_opd.patient.last_name else " ",
        ]
    )
    context["address"] = "".join(
        [
            " ",
            patient_opd.patient.city.city_name
            if patient_opd.patient.city.city_name
            else " ",
            " ",
            patient_opd.patient.district.district_name
            if patient_opd.patient.district.district_name
            else " ",
            " ",
            patient_opd.patient.taluka.taluka_name
            if patient_opd.patient.taluka.taluka_name
            else " ",
            " ",
            patient_opd.patient.state.state_name
            if patient_opd.patient.state.state_name
            else " ",
        ]
    )

    context["husband_name"] = patient_opd.patient.husband_father_name
    context["week_of_pregnancy"] = consultation.lmp_date
    context["mobile_no"] = (
        patient_opd.patient.phone if "F" not in patient_opd.patient.phone else " "
    )
    context["procedure_date"] = usg_form.procedure_date
    context["result_conveyed_to"] = usg_form.result_of_diagnostic_conveyed_to

    context["consent_date"] = usg_form.consent_obtained_date
    context["last_week_of_pregnancy"] = usg_form.procedure_date
    context["consent_obtained_date"] = usg_form.consent_obtained_date
    context["report_date"] = str(patient_opd.opd_date)
    context["ultrasonic_result"] = f"MTP : RESULT OF SONOGRAPHY {usg_form.ut_weeks} weeks preganancy"
    context["any_indication_mtp"] = usg_form.any_indication_mtp.field_value

    context["report_date"] = str(patient_opd.opd_date)
    template_name = "reports/en/usgform_rpt.html"
    return render(request, template_name, {"context": context})
