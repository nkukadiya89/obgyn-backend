from ast import Delete
from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_prescription.models import PatientPrescriptionModel
from patient_voucher.models import PatientVoucherModel, VoucherItemModel
from consultation.models import ConsultationModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def medicine_prescription_rpt(request,voucher_id, language_id=None):

    patient_voucher = PatientVoucherModel.objects.filter(pk=voucher_id).first()

    if patient_voucher == None:
        context = {}
        context["msg"] = False
        context["error"] = "Record does not exist.."
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


    patient_opd = patient_voucher.patient_opd

    if patient_opd == None:
        context = {}
        context["msg"] = False
        context["error"] = "OPD does not exist.."
        return JsonResponse(context)

    consultation = ConsultationModel.objects.filter(patient_opd=patient_opd,deleted=0).first()
    if consultation == None:
        context = {}
        context["msg"] = False
        context["error"] = "Consultation does not exist.."
        return JsonResponse(context)

    if patient_voucher:

        voucher_item_list = VoucherItemModel.objects.filter(patient_voucher=patient_voucher,deleted=0)

        if len(voucher_item_list)<=0:
            context = {}
            context["msg"] = False
            context["error"] = "Record not Found."
            return JsonResponse(context)

        context = {}
        context["receipt_date"] = patient_voucher.bill_date
        context["bill_no"] = patient_voucher.voucher_no
        context["hb"] = consultation.hb
        context["blood_group"] = consultation.blood_group
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
        
        context["mobile"] = patient_opd.patient.phone if "F" not in patient_opd.patient.phone else " "

        medicine =[]
        for voucher_item in voucher_item_list:
            context_sub={}
            context_sub["medicine"] = voucher_item.surgical_item.drug_name
            context_sub["unit"] = voucher_item.unit
            medicine.append(context_sub)
      
        context["medicine"] = medicine
    
    template_name = "reports/en/medicine_prescription.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
