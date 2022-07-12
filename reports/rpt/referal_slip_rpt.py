from django.shortcuts import render
from manage_fields.models import ManageFieldsModel
from template_header.models import TemplateHeaderModel
from patient_referal.models import PatientReferalModel, PatientReferalIndication

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def referal_slip_rpt(request, opd_id, language_id=None):
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id, deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    patient_referal = PatientReferalModel.objects.filter(patient_opd=opd_id, deleted=0).first()
    if not patient_referal:
        context = {}
        context["msg"] = False
        context["error"] = "Record Not found."
        return JsonResponse(context)
    

    patient_opd = patient_referal.patient_opd


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

    context["mobile_no"] = patient_opd.patient.phone if "F" not in patient_opd.patient.phone else " "
    context["age"] = patient_opd.patient.age
    context["referal_date"] = patient_opd.opd_date
    
    indication = list(PatientReferalIndication.objects.filter(patientreferalmodel=patient_referal.patient_referal_id).values_list("managefieldsmodel_id",flat=True))
    indication_list = list(ManageFieldsModel.objects.filter(mf_id__in=indication).values_list('field_value',flat=True))
    context["indication"] = indication_list
    context["referal_date"] = patient_opd.opd_date
    

    template_name = "reports/en/referal_slip.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
