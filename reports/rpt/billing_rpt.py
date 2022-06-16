from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient.models import PatientModel
from patient_billing.models import PatientBillingModel
from user.models import User
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def billing_rpt(request, start_date=None, end_date=None, language_id=1):
    
    patient_billing_list = PatientBillingModel.objects.filter(created_by=request.user.id, deleted=0)
    if start_date and not end_date:
        patient_billing_list = patient_billing_list.filter(created_at__date=start_date)
    elif start_date and end_date:
        patient_billing_list = patient_billing_list.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

    context_list=[]

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Template not found."
        return JsonResponse(context)


    for patient_billing in patient_billing_list:
        patient = patient_billing.patient
        
        context = {}

        context["invoice_no"] = patient_billing.invoice_no
        context["admission_date"] = patient_billing.admission_date
        context["admission_time"] = patient_billing.admission_time
        context["discharge_date"] = patient_billing.discharge_date
        context["discharge_time"] = patient_billing.discharge_time
        context["procedure_name"] = patient_billing.procedure_name
        context["no_of_visit"] = patient_billing.no_of_visit
        context["rs_per_visit"] = patient_billing.rs_per_visit
        context["consulting_fees"] = patient_billing.consulting_fees
        context["usg_rs"] = patient_billing.usg_rs
        context["room_type"] = patient_billing.room_type
        context["room_no_of_day"] = patient_billing.room_no_of_day
        context["room_rs"] = patient_billing.room_rs
        context["procedure_charge"] = patient_billing.procedure_charge
        context["medicine_rs"] = patient_billing.medicine_rs
        context["nursing_rs"] = patient_billing.nursing_rs
        context["other_rs"] = patient_billing.other_rs
        context["total_rs"] = patient_billing.total_rs
        context["no_of_usg"] = patient_billing.no_of_usg
        context_list.append(context)

    template_name = "reports/en/billing_report.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})
