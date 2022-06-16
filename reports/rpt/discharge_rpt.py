from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def discharge_rpt(request, id, language_id=None):
    patient_opd = PatientOpdModel.objects.filter(pk=id,deleted=0).select_related('patientdischargemodel').first()
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Template not found."
        return JsonResponse(context)

    context = {}
    context["name"] = "".join(
        [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
    context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                  patient_opd.patient.district.district_name, " ",
                                  patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])

    context["admission_date"] = str(patient_opd.patientdischargemodel.admission_date) + " " + str(
        patient_opd.patientdischargemodel.admission_time)
    context["discharge_date"] = str(patient_opd.patientdischargemodel.discharge_date) + " " + str(
        patient_opd.patientdischargemodel.discharge_time)
    context["complain_of"] = patient_opd.patientdischargemodel.complain_of
    context["diagnosis"] = patient_opd.patientdischargemodel.diagnosis.diagnosis_name
    context["ot_time_date"] = str(patient_opd.patientdischargemodel.ot_date) + " " + str(
        patient_opd.patientdischargemodel.ot_time)
    context["treatment_given"] = patient_opd.patientdischargemodel.treatment_given
    context["advice"] = patient_opd.patientdischargemodel.advice.field_value
    context["remark"] = patient_opd.patientdischargemodel.remark
    context["name_of_procedure"] = patient_opd.patientdischargemodel.name_of_operation
    template_name = "reports/en/discharge_card.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
