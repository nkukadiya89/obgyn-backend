from re import T
from django.shortcuts import render

from consultation.models import ConsultationModel
from patient_indoor.models import PatientIndoorModel, IndoorAdviceModel
from user.models import User

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def indoor_case_rpt(request, opd_id, language_id=None):

    patient_indoor_list = PatientIndoorModel.objects.filter(patient_opd_id=opd_id).order_by('created_at')


    consultation = ConsultationModel.objects.filter(patient_opd_id = opd_id, deleted=0).first()
    context = {}
    context_list = []
    for patient_indoor in patient_indoor_list:
        context_sub = {}
        patient_opd = patient_indoor.patient_opd

        context_sub["date"] = patient_indoor.indoor_date
        context_sub["time"] = patient_indoor.indoor_time
        context_sub["complain"] =patient_indoor.complain
        context_sub["temp"] = patient_indoor.temprature
        context_sub["pulse"] = patient_indoor.pulse
        context_sub["spo2"] = patient_indoor.spo2
        context_sub["bp"] = patient_indoor.bp
        context_sub["pallor"] = patient_indoor.pallor
        context_sub["lcterus"] = patient_indoor.lcterus
        context_sub["oedema"] = patient_indoor.oedema
        context_sub["rs"] = patient_indoor.rs
        context_sub["cvs"] = patient_indoor.cvs
        context_sub["pa"] = patient_indoor.pa_gyn if consultation.patient_type == "GYN" else patient_indoor.pa_obs
        context_sub["ps"] = patient_indoor.ps.field_value
        context_sub["pv"] = patient_indoor.pv.field_value
        
        context_sub["advice_list"] = list(IndoorAdviceModel.objects.filter(patient_indoor=patient_indoor,deleted=0).select_related('advice').values_list("advice__advice",flat=True))
        context_list.append(context_sub)
    context["context_list"] = context_list


    print(context)

    template_name = "reports/en/indoor_case.html"
    return render(request, template_name,
                  {"context_list": context,})
