from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_mtp.models import PatientMtpModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mtp_list_rpt(request, id, language_id=None):
    from_date = request.body.get('from_date')
    to_date = request.body.get('to_date')

    patient_mtp_list = PatientMtpModel.objects.all()


    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()

    context_list=[]
    for patient_mtp in patient_mtp_list:
        patient_opd_id=patient_mtp.patient_opd_id
        patient_opd = PatientOpdModel.objects.filter(pk=patient_opd_id).select_related('patientdischargemodel').first()

        context = {}
        context["date_of_admission"] = patient_opd.patientdischargemodel.admission_date
        context["name"] = "".join(
            [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
        context["husband_name"] = patient_opd.patient.husband_father_name
        context["age"] = patient_opd.patient.age
        context["religion"] = patient_opd.patient.religion
        context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                      patient_opd.patient.district.district_name, " ",
                                      patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])
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
