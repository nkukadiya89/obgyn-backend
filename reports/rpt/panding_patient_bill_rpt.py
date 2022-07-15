from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def panding_patient_bill_rpt(request, start_date=None, end_date=None, language_id=1):

    patient_billing_list = PatientBillingModel.objects.filter(created_by=request.user.id, deleted=0)
    if start_date and not end_date:
        patient_billing_list = patient_billing_list.filter(created_at__date=start_date)
    elif start_date and end_date:
        patient_billing_list = patient_billing_list.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

    context_list=[]

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)


    context_list = []
    for patient_billing in patient_billing_list:
        patient_opd_id = patient_billing.patient_opd_id 
        patient_opd = PatientOpdModel.objects.filter(pk=patient_opd_id).first()

        if patient_opd:

            context = {}
            context["total_rs"] = patient_billing.total_rs
            # context["patient_opd"] = patient_billing.patient_opd
            # context["date_of_admission"] = patient_billing.admission_date

            context["name"] = "".join(
                [
                    patient_opd.patient.first_name
                    if patient_opd.patient.first_name
                    else " ",
                    " ",
                    patient_opd.patient.middle_name
                    if patient_opd.patient.middle_name
                    else " ",
                    " ",
                    patient_opd.patient.last_name
                    if patient_opd.patient.last_name
                    else " ",
                ]
            )
            context["is_paid"] = (
                patient_opd.is_paid
                if patient_opd.is_paid == False
                else " "
            )
            
        context_list.append(context)
        
    template_name = "reports/en/panding_patient_billing.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})