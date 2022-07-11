from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_mtp.models import PatientMtpModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def mtp_list_rpt(request, start_date, end_date, language_id=None):
    patient_mtp_list = PatientMtpModel.objects.filter(
        created_at__date__gte=start_date, created_at__date__lte=end_date, deleted=0
    )

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

    context_list = []
    for patient_mtp in patient_mtp_list:
        patient_opd_id = patient_mtp.patient_opd_id
        patient_opd = PatientOpdModel.objects.filter(pk=patient_opd_id).first()

        if patient_opd:

            context = {}
            context["date_of_admission"] = patient_mtp.admission_date

            context["name"] = "".join(
                [
                    patient_opd.patient.first_name
                    if patient_opd.patient.first_name
                    else " ",
                    " ",
                    patient_opd.patient.middle_name
                    if patient_opd.patient.middle_name
                    else " ",
                    " ",
                    patient_opd.patient.last_name
                    if patient_opd.patient.last_name
                    else " ",
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
            context["husband_name"] = (
                patient_opd.patient.husband_father_name
                if patient_opd.patient.husband_father_name
                else " "
            )
            context["age"] = patient_opd.patient.age
            context["religion"] = (
                patient_opd.patient.religion.field_value
                if patient_opd.patient.religion.field_value
                else " "
            )

            context["duration"] = patient_mtp.ut_weeks
            context["reason"] = patient_mtp.reason_for_mtp
            context["termination_date"] = patient_mtp.termination_date
            context["discharge_date"] = patient_mtp.discharge_date
            context["remark"] = patient_mtp.remark
            context["opinion_by_name"] = patient_mtp.second_rmp

            if patient_opd.consulted_by:
                context["terminated_by"] = "".join(
                    [
                        patient_opd.consulted_by.first_name
                        if patient_opd.consulted_by.first_name
                        else " ",
                        " ",
                        patient_opd.consulted_by.middle_name
                        if patient_opd.consulted_by.middle_name
                        else " ",
                        " ",
                        patient_opd.consulted_by.last_name
                        if patient_opd.consulted_by.last_name
                        else " ",
                    ]
                )
            else:
                context["terminated_by"] = ""
            context_list.append(context)
    template_name = "reports/en/mtp_list.html"
    return render(
        request,
        template_name,
        {
            "context_list": context_list,
            "template_header": template_header.header_text.replace("'", '"'),
        },
    )
