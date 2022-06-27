from email.mime import image
from django.shortcuts import render, HttpResponse
from rest_framework import status
from patient_opd.models import PatientOpdModel
from template_header.models import TemplateHeaderModel
from consultation.models import ConsultationModel
from language.models import LanguageModel
from django.views.decorators.csrf import csrf_exempt
from utility.aws_file_upload import upload_barcode_image
from patient_prescription.models import PatientPrescriptionModel
from django.http import JsonResponse



@csrf_exempt
def consultation_rpt(request, id, language_id=None):
    
    consultation = ConsultationModel.objects.filter(pk=id,deleted=0).first()
    if consultation == None:
        return HttpResponse("Consultation Record Does not exist", status=status.HTTP_400_BAD_REQUEST)

    language = LanguageModel.objects.filter(pk=language_id).first()

    if language == None:
        return HttpResponse("Invalid Language selected", status=status.HTTP_400_BAD_REQUEST)


    patient_opd = PatientOpdModel.objects.filter(pk=consultation.patient_opd_id)


    if len(patient_opd) == 0:
        return HttpResponse("OPD Record Does not exist", status=status.HTTP_400_BAD_REQUEST)

    patient_opd = patient_opd.first()

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(created_by=request.user.id,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Please create report header."
        return JsonResponse(context)


        
    context = {}
    context["receipt_date"] = str(patient_opd.opd_date)
    context["regd_no"] = patient_opd.patient.regd_no_barcode


    consultation = ConsultationModel.objects.filter(patient_opd=patient_opd).first()
    
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

    context["mobile_no"] = patient_opd.patient.phone

    context["report_date"] = str(patient_opd.opd_date)

    context["hb"] = consultation.hb

    context["ho"] = consultation.ho.field_value
    context["blood_group"] = consultation.blood_group
    context["co"] = consultation.co.field_value
    context["age"] = patient_opd.patient.age
    context["mh"] = "--NA--"
    context["lmp"] = consultation.lmp_date
    context["edd"] = consultation.edd_date
    context["edds"] = consultation.possible_edd
    context["ohml"] = "--NA--"
    context["ftnd_male_live"] = consultation.ftnd_male_live
    context["ftnd_male_dead"] = consultation.ftnd_male_dead
    context["ftnd_female_live"] = consultation.ftnd_female_live
    context["ftnd_female_dead"] = consultation.ftnd_female_dead
    context["ftlscs_male_live"] = consultation.ftlscs_male_live
    context["ftlscs_male_dead"] = consultation.ftlscs_male_dead
    context["ftlscs_female_live"] = consultation.ftlscs_female_live
    context["ftlscs_female_dead"] = consultation.ftlscs_female_dead

    context["phfh"] = consultation.fhs
    context["tprbp"] = "/".join(
        [str(consultation.temprature), str(consultation.puls),
         str(consultation.resperistion),
         str(consultation.bp)])
    context["pio"] = "--NA--"
    context["rscvs"] = consultation.rs + "/" + consultation.cvs
    context["pa"] = consultation.pa_value
    context["ps"] = consultation.ps.field_value
    context["pv"] = consultation.pv.field_value

    prescription_list = PatientPrescriptionModel.objects.filter(consultation=consultation)

    context_sub = []
    for prescription in prescription_list:
        prescribe = {}
        prescribe["type"] = prescription.medicine.medicine_type.medicine_type
        prescribe["medicine"] = prescription.medicine.medicine
        prescribe["total"] = prescription.medicine.total_tablet

        context_sub.append(prescribe)

    context["prescription"] = context_sub
    template_name = "reports/en/consultation.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
