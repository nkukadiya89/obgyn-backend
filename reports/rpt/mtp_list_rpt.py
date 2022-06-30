from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_mtp.models import PatientMtpModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def mtp_list_rpt(request, language_id=None):
    patient_mtp_list = PatientMtpModel.objects.filter(deleted=0)

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    context_list=[]
    for patient_mtp in patient_mtp_list:
        patient_opd_id=patient_mtp.patient_opd_id
        patient_opd = PatientOpdModel.objects.filter(pk=patient_opd_id).first()

        if patient_opd:
            
            context = {}
            context["date_of_admission"] = patient_opd.patientdischargemodel.admission_date

            try:
                context["name"] = "".join(
                    [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
                context["husband_name"] = patient_opd.patient.husband_father_name
                context["age"] = patient_opd.patient.age
                context["religion"] = patient_opd.patient.religion.field_value
                context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                            patient_opd.patient.district.district_name, " ",
                                            patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])
            except:
                context["name"] = ""
                context["husband_name"] = ""
                context["age"] =""
                context["religion"] = ""
                context["address"] = ""
                
            context["duration"] = "pending"
            context["reason"] = patient_mtp.reason_for_mtp
            context["termination_date"] = patient_mtp.termination_date
            context["discharge_date"] = patient_mtp.discharge_date
            context["remark"] = patient_mtp.remark
            context["opinion_by_name"] = "fix to be changed"
            context["terminated_by"] = "fix to be changed"
            context_list.append(context)
    template_name = "reports/en/mtp_list.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})
