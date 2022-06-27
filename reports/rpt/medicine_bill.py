from ast import Delete
from django.shortcuts import render
from patient_voucher.models import PatientVoucherModel, VoucherItemModel
from template_header.models import TemplateHeaderModel
from patient_prescription.models import PatientPrescriptionModel
from patient_opd.models import PatientOpdModel
from consultation.models import ConsultationModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def medicine_bill_rpt(request,bill_id, language_id=None):

    patient_voucher = PatientVoucherModel.objects.filter(pk=bill_id).first()

    if patient_voucher == None:
        context = {}
        context["msg"] = False
        context["error"] = "Bill does not exist.."
        return JsonResponse(context)

    patient_opd =patient_voucher.patient_opd

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)

    consultation = ConsultationModel.objects.filter(patient_opd=patient_opd,deleted=0).first()
    if patient_opd:
        voucher_item_list = VoucherItemModel.objects.filter(patient_voucher=patient_voucher,deleted=0)

        if len(voucher_item_list)<=0:
            context = {}
            context["msg"] = False
            context["error"] = "Record not Found."
            return JsonResponse(context)

        context = {}
        context["receipt_date"] = patient_voucher.created_at.date()
        context["bill_no"] = patient_voucher.voucher_no

        if consultation:
            context["hb"] = consultation.hb
            context["blood_group"] = consultation.blood_group
        else:
            context["hb"] = ""
            context["blood_group"] = ""

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
                
        context["mobile"] = patient_opd.patient.phone

        medicine =[]
        total=0
        for voucher_item in voucher_item_list:
            context_sub={}
            context_sub["medicine"] = voucher_item.surgical_item.drug_name
            context_sub["unit"] = voucher_item.unit
            context_sub["rate"] = voucher_item.rate
            context_sub["mfg_date"] = voucher_item.surgical_item.mfg_date
            context_sub["exp_date"] = voucher_item.surgical_item.exp_date
            context_sub["total"] = voucher_item.total_amount
            total = total + voucher_item.total_amount
            medicine.append(context_sub)
        context["final_total"] = total
        context["medicine"] = medicine
        context["medicine_count"] = len(voucher_item_list)
    template_name = "reports/en/medicine_bill.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
