from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel
from patient_opd.models import PatientOpdModel
from consultation.models import ConsultationModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def hospital_bill_rpt(request,bill_no, language_id=None):

    patient_billing =PatientBillingModel.objects.filter(patient_billing_id=bill_no).first()

    if patient_billing == None:
        context = {}
        context["msg"] = False
        context["error"] = "Patient Bill does not exist.."
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

    context_list=[]

    patient_opd = patient_billing.patient_opd

    if patient_opd:
        
        context = {}
        context["receipt_date"] = patient_billing.created_at
        context["invoice_no"] = patient_billing.invoice_no
        context["name"] = "".join(
            [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])

        try:
            context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                        patient_opd.patient.district.district_name, " ",
                                        patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])
        except:
            context["address"] = ""
        
        context["mobile"] = patient_opd.patient.phone
        consultation = ConsultationModel.objects.filter(patient_opd=patient_opd).first()

        if consultation:
            context["blood_group"] = consultation.blood_group
            context["diagnosis"] = consultation.diagnosis.diagnosis_name
        else:
            context["blood_group"] = ""
            context["diagnosis"] = ""
        
        context["admission_date"] = patient_billing.admission_date
        context["discharge_date"] = patient_billing.discharge_date
        context["consulting_rs"] = patient_billing.consulting_fees
        context["sonography_rs"] = patient_billing.usg_rs
        context["nursing_rs"] = patient_billing.nursing_rs
        context["operative_rs"] = patient_billing.procedure_charge
        context["medicine_rs"] = patient_billing.medicine_rs
        context["room_charge_rs"] = patient_billing.room_rs
        context["other_charge_rs"] = patient_billing.other_rs
        context["total_rs"] = patient_billing.total_rs
        
    template_name = "reports/en/hospital_bill.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
