from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_billing.models import PatientBillingModel
from patient_opd.models import PatientOpdModel
from consultation.models import ConsultationModel
from patient_voucher.models import PatientVoucherModel

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
        
        context["mobile"] = patient_opd.patient.phone if "F" not in patient_opd.patient.phone else ""
        consultation = ConsultationModel.objects.filter(patient_opd=patient_opd).first()


        if consultation:
            context["blood_group"] = consultation.blood_group
            context["diagnosis"] = consultation.diagnosis.diagnosis_name
        else:
            context["blood_group"] = ""
            context["diagnosis"] = ""
        
        total=0
        context["admission_date"] = patient_billing.admission_date
        context["admission_time"] = patient_billing.admission_time
        context["discharge_date"] = patient_billing.discharge_date
        context["discharge_time"] = patient_billing.discharge_time
        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="C",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}
        context["consulting_rs"] = voucher_detail

        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="S",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}

        context["sonography_rs"] = voucher_detail

        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="N",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}
        context["nursing_rs"] = voucher_detail

        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="O",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}
        context["operative_rs"] = voucher_detail

        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="M",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}
        context["medicine_rs"] = voucher_detail

        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="R",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}
        context["room_charge_rs"] = voucher_detail

        voucher = PatientVoucherModel.objects.filter(patient_opd=patient_opd,voucher_type="E",deleted=0).last()
        if voucher:
            voucher_detail={"no":voucher.voucher_no ,"amount":voucher.amount}
            total += float(voucher.amount)
        else:
            voucher_detail={"no":"" ,"amount":0}
        context["other_charge_rs"] = voucher_detail

        context["total_rs"] = total
        
    template_name = "reports/en/hospital_bill.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
