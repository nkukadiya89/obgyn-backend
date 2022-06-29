from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_indoor.models import PatientIndoorModel
from user.models import User

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def indoor_case_paper_rpt(request, case_no, language_id=None):

    patient_indoor = PatientIndoorModel.objects.filter(pk=case_no).first()

    if not patient_indoor:
        context = {}
        context["msg"] = False
        context["error"] = "Indoor case no does not exist."
        return JsonResponse(context)

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id, deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    context = {}

    patient_opd = patient_indoor.patient_opd
    context["regd_no"] = patient_opd.patient.regd_no_barcode

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

    context["husband_name"] = patient_opd.patient.husband_father_name
    context["age"] = patient_opd.patient.age
    context["gender"] = patient_opd.patient.gender
    context["admission_date"] = patient_indoor.adm_date
    context["admission_time"] = patient_indoor.adm_time
    
    doctor = User.objects.filter(pk=patient_opd.consulted_by_id).first()
    if doctor:
        context["doctor"] = "".join([doctor.first_name, " ", doctor.middle_name, " ", doctor.last_name])
    else:
        context["doctor"] = ""
    
    context["provisional_diagnosis"] = patient_indoor.provisional_diagnosis.field_value
    context["operation"] = patient_indoor.operation.field_value
    context["operation_date"] = patient_indoor.oper_date
    context["operation_time"] = patient_indoor.oper_time
    context["surgeon_name"] = "Nirav Kukadiya"
    context["anesthetist_name"] = "Nirav Kukadiya"
    context["final_diagnosis"] = "Final diagnosis to be filled"
    context["discharge_date"] = patient_indoor.disch_date
    context["discharge_time"] = patient_indoor.disch_time
    context["discharge_condition"] = "D/C pending"
    context["advised"] = "advised pending"




    template_name = "reports/en/indoor_case_paper.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
