from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_mtp.models import PatientMtpModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def daily_opd_income_rpt(request, rpt_date=None, language_id=None):

    patient_otp_list = PatientOpdModel.objects.filter(deleted=0)

    if rpt_date:
        patient_otp_list = patient_otp_list.filter(created_at__date=rpt_date)


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
    for patient_opd in patient_otp_list:
        patient_opd_id=patient_opd.patient_opd_id

        
        if patient_opd:
            
            context = {}
            context["date"] = patient_opd.created_at
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
            context["type"] = "consultation"
            context["col1_total"] = 0
            context["col2_total"] = 0
            context["col3_total"] = 0
            context["col4_total"] = 0
            context["col5_total"] = 0
            context["col6_total"] = 0
            context["col7_total"] = 0
            context["col8_total"] = 0

            try:
                context["consulting"] = patient_opd.patientbillingmodel_set.consulting_fees
                context["sonography"] = patient_opd.patientbillingmodel_set.usg_rs
                context["nursing"] = patient_opd.patientbillingmodel_set.nursing_rs
                context["operative"] = patient_opd.patientbillingmodel_set.procedure_charge
                context["medicine"] = patient_opd.patientbillingmodel_set.medicine_rs
                context["room_charge"] = patient_opd.patientbillingmodel_set.room_rs
                context["other_charge"] = patient_opd.patientbillingmodel_set.other_rs
                context["total"] = patient_opd.patientbillingmodel_set.total_rs
            except:
                context["consulting"] = 0
                context["sonography"] = 0
                context["nursing"] = 0
                context["operative"] = 0
                context["medicine"] = 0
                context["room_charge"] = 0
                context["other_charge"] = 0
                context["total"] = 0
                
            context["col1_total"] = float(context["col1_total"]) + float(context["consulting"])
            context["col2_total"] = float(context["col2_total"]) + float(context["sonography"])
            context["col3_total"] = float(context["col3_total"]) + float(context["nursing"])
            context["col4_total"] = float(context["col4_total"]) + float(context["operative"])
            context["col5_total"] = float(context["col5_total"]) + float(context["medicine"])
            context["col6_total"] = float(context["col6_total"]) + float(context["room_charge"])
            context["col7_total"] = float(context["col7_total"]) + float(context["other_charge"])
            context["col8_total"] = float(context["col8_total"]) + float(context["total"])


            context_list.append(context)
    template_name = "reports/en/daily_opd_income.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})
