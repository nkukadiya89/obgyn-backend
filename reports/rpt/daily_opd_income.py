from django.shortcuts import render
import consultation
from consultation.models import ConsultationModel
import patient_billing
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel
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
    context = {}
    context["col1_total"] = 0
    context["col2_total"] = 0
    context["col3_total"] = 0
    context["col4_total"] = 0
    context["col5_total"] = 0
    context["col6_total"] = 0
    context["col7_total"] = 0
    context["col8_total"] = 0
    context["col9_total"] = 0

    for patient_opd in patient_otp_list:
        patient_opd_id=patient_opd.patient_opd_id

        consultation = ConsultationModel.objects.filter(patient_opd=patient_opd).first()

        patient_billing_list = PatientBillingModel.objects.filter(deleted=0,patient_opd=patient_opd)
        for patient_billing in patient_billing_list:            
            context_sub={}
            context_sub["date"] = patient_opd.created_at
            context_sub["name"] = "".join(
                [
                    patient_opd.patient.first_name  if patient_opd.patient.first_name else " ",
                    " ",
                    patient_opd.patient.middle_name if patient_opd.patient.middle_name else " ",
                    " ",
                    patient_opd.patient.last_name if patient_opd.patient.last_name else " ",
                ]
            )
            context_sub["address"] = "".join(
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

            if consultation.patient_type == "OB":
                context_sub["type"] = "Obstract"
            else:
                context_sub["type"] = "Gynec"


            try:
                context_sub["payment"] = patient_billing.payment
                context_sub["consulting"] = patient_billing.consulting_fees
                context_sub["sonography"] = patient_billing.usg_rs
                context_sub["nursing"] = patient_billing.nursing_rs
                context_sub["operative"] = patient_billing.procedure_charge
                context_sub["medicine"] = patient_billing.medicine_rs
                context_sub["room_charge"] = patient_billing.room_rs
                context_sub["other_charge"] = patient_billing.other_rs
                context_sub["total"] = patient_billing.total_rs
            except:
                context_sub["payment"] = 0
                context_sub["consulting"] = 0
                context_sub["sonography"] = 0
                context_sub["nursing"] = 0
                context_sub["operative"] = 0
                context_sub["medicine"] = 0
                context_sub["room_charge"] = 0
                context_sub["other_charge"] = 0
                context_sub["total"] = 0
                
            context["col1_total"] = float(context["col1_total"]) + patient_billing.consulting_fees
            context["col2_total"] = float(context["col2_total"]) + patient_billing.usg_rs
            context["col3_total"] = float(context["col3_total"]) + patient_billing.nursing_rs
            context["col4_total"] = float(context["col4_total"]) + patient_billing.procedure_charge
            context["col5_total"] = float(context["col5_total"]) + patient_billing.medicine_rs
            context["col6_total"] = float(context["col6_total"]) + patient_billing.room_rs
            context["col7_total"] = float(context["col7_total"]) + patient_billing.other_rs
            context["col8_total"] = float(context["col8_total"]) + patient_billing.total_rs


            context_list.append(context_sub)
    context["context_list"] = context_list
    template_name = "reports/en/daily_opd_income.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
