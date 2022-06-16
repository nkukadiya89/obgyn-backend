from django.shortcuts import render, HttpResponse

from rest_framework import status
from patient_opd.models import PatientOpdModel
from template_header.models import TemplateHeaderModel
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def usg_rpt(request, id, language_id=None):
    patient_opd = PatientOpdModel.objects.filter(pk=id,deleted=0).select_related('consultationmodel')

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Template not found."
        return JsonResponse(context)

    patient_opd = patient_opd.first()
    if patient_opd == None:
        return HttpResponse("Record Does not exist", status=status.HTTP_400_BAD_REQUEST)

    template_name = "reports/en/usg_report.html"
    context = {}
    context["receipt_date"] = str(patient_opd.opd_date)
    context["regd_no"] = patient_opd.patient.regd_no_barcode
    context["hb"] = ""
    context["name"] = "".join(
        [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
    context["mobile_no"] = patient_opd.patient.phone
    context["blood_group"] = patient_opd.consultationmodel.hb
    context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                  patient_opd.patient.district.district_name, " ",
                                  patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])
    context["report_date"] = str(patient_opd.opd_date)
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
