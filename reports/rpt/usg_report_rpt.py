from django.shortcuts import render, HttpResponse

from rest_framework import status
from consultation.models import ConsultationModel
from patient_opd.models import PatientOpdModel
from patient_usgreport.models import PatientUSGReportModel
from template_header.models import TemplateHeaderModel
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def usg_rpt(request, id, language_id=None):
    usg_report = PatientUSGReportModel.objects.filter(pk=id,deleted=0).first()
    if usg_report == None:
        context = {}
        context["msg"] = False
        context["error"] = "Record Does not exist."
        return JsonResponse(context)

    patient_opd = usg_report.patient_opd

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    patient_opd = patient_opd
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


    template_name = "reports/en/usg_report.html"
    context = {}
    context["receipt_date"] = patient_opd.opd_date
    context["regd_no"] = patient_opd.patient.regd_no_barcode


    if consultation:
        context["hb"] = consultation.hb
        context["blood_group"] = consultation.blood_group
    else:
        context["hb"] =""
        context["blood_group"] =""

    context["name"] = "".join(
        [
            patient_opd.patient.first_name  if patient_opd.patient.first_name else " ",
            " ",
            patient_opd.patient.middle_name if patient_opd.patient.middle_name else " ",
            " ",
            patient_opd.patient.last_name if patient_opd.patient.last_name else " ",
        ]
    )
    context["address"] = "".join(
        [
            " ",
            patient_opd.patient.city.city_name if patient_opd.patient.city.city_name else " ",
            " ",
            patient_opd.patient.district.district_name if patient_opd.patient.district.district_name else " ",
            " ",
            patient_opd.patient.taluka.taluka_name if patient_opd.patient.taluka.taluka_name else " ",
            " ",
            patient_opd.patient.state.state_name if patient_opd.patient.state.state_name else " ",
        ]
    )
    context["remark"] = usg_report.remark
    context["mobile_no"] = patient_opd.patient.phone if "F" not in patient_opd.patient.phone else " "
    context["report_detail"] = f"""A {usg_report.no_of_foetus} intrauterine foctus/s with {usg_report.cardiac_activity} cardiac activity
    with {usg_report.presentation} presentation.
    with avg. {usg_report.avg_weeks} weeks of gestational age.
    GS {usg_report.ga_weeks} weeks and {usg_report.ga_day} day
    CRL {usg_report.crl_weeks} weeks and {usg_report.crl_day} day
    FL {usg_report.fl_weeks} weeks and {usg_report.fl_day} day
    BPD {usg_report.bpd_weeks} weeks and {usg_report.bpd_day} day
    HC {usg_report.hc_weeks} weeks and {usg_report.hc_day} day
    AC {usg_report.ac_weeks} weeks and {usg_report.ac_day} day
    AVG {usg_report.avg_weeks} weeks and {usg_report.avg_day} day
    Placenta - {usg_report.placental_location.field_value}
    Liquar - {usg_report.amount_of_liquor }
    {usg_report.anomalies.field_value if usg_report.anomalies.field_value else " "}"""

    context["avg_edd"] = usg_report.avg_edd
    context["possible_lmp"] = usg_report.possible_lmp

    context["report_date"] = patient_opd.opd_date
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
