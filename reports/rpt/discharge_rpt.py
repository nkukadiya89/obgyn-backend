from django.shortcuts import render
from patient_discharge.models import PatientDischargeModel
from template_header.models import TemplateHeaderModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def discharge_rpt(request, id, language_id=None):
    patient_opd = PatientOpdModel.objects.filter(pk=id, deleted=0).first()
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

    if not patient_opd:
        context = {}
        context["msg"] = False
        context["error"] = "OPD not found."
        return JsonResponse(context)

    context = {}
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

    patient_discharge = PatientDischargeModel.objects.filter(
        patient_opd=patient_opd
    ).first()
    
    if patient_discharge == None:
        context = {}
        context["msg"] = False
        context["error"] = "Patient Discharge Does not exist."
        return JsonResponse(context)

    if patient_discharge:
        context["admission_date"] = (
            str(patient_discharge.admission_date.strftime("%d-%m-%Y"))
            + " "
            + str(patient_discharge.admission_time)
        )
        context["discharge_date"] = (
            str(patient_discharge.discharge_date.strftime("%d-%m-%Y"))
            + " "
            + str(patient_discharge.discharge_time)
        )
        context["complain_of"] = patient_discharge.complain_of.field_value if patient_discharge.complain_of.field_value else " "
        context["diagnosis"] = patient_discharge.diagnosis.diagnosis_name
        context["ot_time_date"] = (
            str(patient_discharge.ot_date.strftime("%d-%m-%Y")) + " " + str(patient_discharge.ot_time)
        )
        context["treatment_given"] = patient_discharge.treatment_given.field_value
        context["advice"] = patient_discharge.advice.field_value if patient_discharge.advice.field_value else " "
        context["remark"] = patient_discharge.remark
        context["name_of_operation"] = patient_discharge.name_of_operation.field_value if patient_discharge.name_of_operation.field_value else " "
    template_name = "reports/en/discharge_card.html"
    return render(
        request,
        template_name,
        {
            "context": context,
            "template_header": template_header.header_text.replace("'", '"'),
        },
    )
