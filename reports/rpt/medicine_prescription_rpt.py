from ast import Delete
from django.shortcuts import render
from template_header.models import TemplateHeaderModel
from patient_prescription.models import PatientPrescriptionModel
from patient_opd.models import PatientOpdModel
from consultation.models import ConsultationModel

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def medicine_prescription_rpt(request,opd_id, language_id=None):

    patient_opd =PatientOpdModel.objects.filter(pk=opd_id).first()

    if patient_opd == None:
        context = {}
        context["msg"] = False
        context["error"] = "Patient OPD does not exist.."
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

    if patient_opd:
        consultation = ConsultationModel.objects.filter(patient_opd=patient_opd,deleted=0).first()

        if not consultation:
            context = {}
            context["msg"] = False
            context["error"] = "Record not Found2."
            return JsonResponse(context)

        patient_prescription_list = PatientPrescriptionModel.objects.filter(consultation=consultation,deleted=0)
        if len(patient_prescription_list)<=0:
            context = {}
            context["msg"] = False
            context["error"] = "Record not Found1."
            return JsonResponse(context)

        context = {}
        context["receipt_date"] = "pending"
        context["bill_no"] = "pending"
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
        
        context["mobile"] = patient_opd.patient.phone

        medicine =[]
        for patient_prescription in patient_prescription_list:
            context_sub={}
            context_sub["medicine"] = patient_prescription.medicine.medicine
            context_sub["unit"] = patient_prescription.medicine.total_tablet
            medicine.append(context_sub)
        
        context["medicine"] = medicine
        print(context)
    template_name = "reports/en/medicine_prescription.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
