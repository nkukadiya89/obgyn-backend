from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def bill_receipt_rpt(request,bill_id, language_id=None):

    patient_billing = PatientBillingModel.objects.filter(pk=bill_id,deleted=0).first()

    if patient_billing == None:
        context = {}
        context["msg"] = False
        context["error"] = "Record Does not exist2."
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

    patient_opd = patient_billing.patient_opd

    if patient_opd:
        
        context = {}
        context["regd_no"] = patient_opd.patient.regd_no_barcode
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

        
        context["bill_no"] = patient_billing.invoice_no
        context["receipt_date"] = patient_billing.invoice_date
        context["total"] = patient_billing.total_rs
        
    template_name = "reports/en/bill_receipt.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
