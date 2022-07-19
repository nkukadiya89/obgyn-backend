from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel
from patient_opd.models import PatientOpdModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def pending_patient_bill_rpt(request, start_date=None, end_date=None, language_id=1):

    context_list = []
    if start_date !=None or end_date!=None :

        if language_id:
            template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
        else:
            template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

        if not template_header:
            context = {}
            context["msg"] = False
            context["error"] = "Please create report header."
            return JsonResponse(context)

        patient_opd_model = PatientOpdModel.objects.filter(created_by=request.user.id, is_paid = False , created_at__date__gte=start_date, created_at__date__lte=end_date, deleted=0)
        
        
        for patient_opd in patient_opd_model:
            context = {}
            context["regd_no"] = patient_opd.patient.regd_no_barcode
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
           
            context_list.append(context)
    else:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    template_name = "reports/en/pending_patient_billing.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})    

 

            

    


