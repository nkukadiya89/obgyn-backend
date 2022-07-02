from ast import Delete
from tracemalloc import start
from django.shortcuts import render
from patient_voucher.models import PatientVoucherModel, VoucherItemModel
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def monthly_income_rpt(request, language_id=None,start_date=None,end_date=None):

    patient_billing_list =PatientBillingModel.objects.filter(invoice_date__gte=start_date,invoice_date__lte=end_date,deleted=0)

    if len(patient_billing_list) <= 0:
        context = {}
        context["msg"] = False
        context["error"] = "No record present."
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


    context={}
    context["start_date"] = datetime.strptime(start_date,"%Y-%m-%d")
    context["end_date"] = datetime.strptime(end_date,"%Y-%m-%d")
    print(context)
    bill_detail = []
    context["col1_total"]=0
    context["col2_total"]=0
    context["col3_total"]=0
    context["col4_total"]=0
    context["col5_total"]=0
    context["col6_total"]=0
    context["col7_total"]=0
    context["col8_total"]=0
    for patient_billing in patient_billing_list:

        patient_opd =patient_billing.patient_opd

        if patient_opd:
            context_sub = {}
            context_sub["date"] = patient_billing.invoice_date
            context_sub["consulting_rs"] = patient_billing.consulting_fees
            context_sub["usg_rs"] = patient_billing.usg_rs
            context_sub["nursing_rs"] = patient_billing.nursing_rs
            context_sub["operative_rs"] = patient_billing.procedure_charge
            context_sub["medicine_rs"] = patient_billing.medicine_rs
            context_sub["room_charge_rs"] = patient_billing.room_rs
            context_sub["other_charge_rs"] = patient_billing.other_rs
            context_sub["total_rs"] = patient_billing.total_rs
            
            context["col1_total"] =context["col1_total"] + patient_billing.consulting_fees
            context["col2_total"] =context["col2_total"] + patient_billing.usg_rs
            context["col3_total"] =context["col3_total"] + patient_billing.nursing_rs
            context["col4_total"] =context["col4_total"] + patient_billing.procedure_charge
            context["col5_total"] =context["col5_total"] + patient_billing.medicine_rs
            context["col6_total"] =context["col6_total"] + patient_billing.room_rs
            context["col7_total"] =context["col7_total"] + patient_billing.other_rs
            context["col8_total"] =context["col8_total"] + patient_billing.total_rs

            bill_detail.append(context_sub)
    
    context["bill_detail"] = bill_detail
    template_name = "reports/en/monthly_income.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
