from django.shortcuts import render, HttpResponse

from rest_framework import status
from consultation.models import ConsultationModel
from patient_opd.models import PatientOpdModel
from patient_usgreport.models import PatientUSGReportModel
from patient_usgform.models import PatientUSGFormModel
from template_header.models import TemplateHeaderModel
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def usg_list_report_rpt(request, language_id=None, start_date=None, end_date=None):

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)



    usg_report_list = PatientUSGFormModel.objects.filter(
        created_at__date__gte=start_date, created_at__date__lte=end_date, deleted=0
    )

    template_name = "reports/en/usg_list_report.html"
    context = {}
    usg_detail = []

    
    for usg_report in usg_report_list:

        consultation = ConsultationModel.objects.filter(
            patient_opd=usg_report.patient_opd
        ).first()

        context_sub = {}
        context_sub["sr_no"] = (
            str(usg_report.serial_no_month) + "/" + str(usg_report.serial_no_year)
        )
        context_sub["usg_date"] = usg_report.created_at.date()
        context_sub["woman_name"] = "".join(
            [
                usg_report.patient_opd.patient.first_name
                if usg_report.patient_opd.patient.first_name
                else " ",
                " ",
                usg_report.patient_opd.patient.middle_name
                if usg_report.patient_opd.patient.middle_name
                else " ",
                " ",
                usg_report.patient_opd.patient.last_name
                if usg_report.patient_opd.patient.last_name
                else " ",
            ]
        )
        context_sub["husband_name"] = (
            usg_report.patient_opd.patient.husband_father_name
            if usg_report.patient_opd.patient.husband_father_name
            else " "
        )
        context_sub["address"] = "".join(
            [
                " ",
                usg_report.patient_opd.patient.city.city_name
                if usg_report.patient_opd.patient.city.city_name
                else " ",
                " ",
                usg_report.patient_opd.patient.district.district_name
                if usg_report.patient_opd.patient.district.district_name
                else " ",
                " ",
                usg_report.patient_opd.patient.taluka.taluka_name
                if usg_report.patient_opd.patient.taluka.taluka_name
                else " ",
                " ",
                usg_report.patient_opd.patient.state.state_name
                if usg_report.patient_opd.patient.state.state_name
                else " ",
            ]
        )
        context_sub["mobile"] = usg_report.patient_opd.patient.phone if "F" not in usg_report.patient_opd.patient.phone else " "
        context_sub["age"] = usg_report.patient_opd.patient.age
        context_sub["live_mf"] = usg_report.live_male_female
        context_sub["pndt"] = "Sonography"

        usg_detail.append(context_sub)
    context["usg_detail"] = usg_detail
    return render(
        request,
        template_name,
        {
            "context": context,
            "template_header": template_header.header_text.replace("'", '"'),
        },
    )
