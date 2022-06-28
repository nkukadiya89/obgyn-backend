from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_ovulation_profile.models import PatientOvulationProfileModel
from consultation.models import ConsultationModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def ovulation_profile_rpt(request,ovulation_id, language_id=None):

    patient_ovulation = PatientOvulationProfileModel.objects.filter(pk=ovulation_id).first()

    if patient_ovulation == None:
        context = {}
        context["msg"] = False
        context["error"] = "Record Does not exist."
        return JsonResponse(context)

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    patient_opd = patient_ovulation.patient_opd

    if patient_opd:
        
        context = {}
        context["name"] = "".join(
            [
                patient_opd.patient.first_name  if patient_opd.patient.first_name else " ",
                " ",
                patient_opd.patient.middle_name if patient_opd.patient.middle_name else " ",
                " ",
                patient_opd.patient.last_name if patient_opd.patient.last_name else " ",
            ]
        )
        
        context["day"] = patient_ovulation.op_day
        context["date"] = patient_ovulation.op_date
        context["right_ovary"] = patient_ovulation.right_ovary_mm
        context["left_ovary"] = patient_ovulation.left_ovary_mm
        context["endometrium"] = patient_ovulation.endometrium_mm
        context["remark"] = patient_ovulation.remark
        context["regd_no"] = patient_opd.patient.regd_no_barcode
        
    template_name = "reports/en/ovulation_profile.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
