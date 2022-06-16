from email.mime import image
from django.shortcuts import render, HttpResponse
from rest_framework import status
from patient_opd.models import PatientOpdModel
from template_header.models import TemplateHeaderModel
from consultation.models import ConsultationModel
from language.models import LanguageModel
from django.views.decorators.csrf import csrf_exempt
from utility.aws_file_upload import upload_barcode_image
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

    patient_opd = patient_opd.select_related('consultationmodel')
    patient_opd = patient_opd.first()

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id,deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1,deleted=0).first()

    if not template_header:
        context = {}
        context["msg"] = False
        context["error"] = "Template not found."
        return JsonResponse(context)


        
    context = {}
    context["receipt_date"] = str(patient_opd.opd_date)
    context["regd_no"] = patient_opd.patient.regd_no_barcode



    

    context["name"] = "".join(
        [patient_opd.patient.first_name if patient_opd.patient.first_name else "", " ", patient_opd.patient.middle_name if patient_opd.patient.middle_name else "", " ", patient_opd.patient.last_name if patient_opd.patient.last_name else ""])
    context["mobile_no"] = patient_opd.patient.phone
    context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                  patient_opd.patient.district.district_name, " ",
                                  patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])

    context["report_date"] = str(patient_opd.opd_date)

    context["hb"] = patient_opd.consultationmodel.hb

    context["ho"] = patient_opd.consultationmodel.ho
    context["blood_group"] = patient_opd.consultationmodel.blood_group
    context["co"] = patient_opd.consultationmodel.co
    context["age"] = patient_opd.patient.age
    context["mh"] = "--NA--"
    context["lmp"] = patient_opd.consultationmodel.lmp_date
    context["edd"] = patient_opd.consultationmodel.edd_date
    context["edds"] = patient_opd.consultationmodel.possible_edd
    context["ohml"] = "--NA--"
    context["ftnd_male_live"] = patient_opd.consultationmodel.ftnd_male_live
    context["ftnd_male_dead"] = patient_opd.consultationmodel.ftnd_male_dead
    context["ftnd_female_live"] = patient_opd.consultationmodel.ftnd_female_live
    context["ftnd_female_dead"] = patient_opd.consultationmodel.ftnd_female_dead
    context["ftlscs_male_live"] = patient_opd.consultationmodel.ftlscs_male_live
    context["ftlscs_male_dead"] = patient_opd.consultationmodel.ftlscs_male_dead
    context["ftlscs_female_live"] = patient_opd.consultationmodel.ftlscs_female_live
    context["ftlscs_female_dead"] = patient_opd.consultationmodel.ftlscs_female_dead

    context["phfh"] = patient_opd.consultationmodel.fhs
    context["tprbp"] = "/".join(
        [str(patient_opd.consultationmodel.temprature), str(patient_opd.consultationmodel.puls),
         str(patient_opd.consultationmodel.resperistion),
         str(patient_opd.consultationmodel.bp)])
    context["pio"] = "--NA--"
    context["rscvs"] = patient_opd.consultationmodel.rs + "/" + patient_opd.consultationmodel.cvs
    context["pa"] = patient_opd.consultationmodel.pa_value
    context["ps"] = patient_opd.consultationmodel.ps
    context["pv"] = patient_opd.consultationmodel.pv

    template_name = "reports/en/consultation.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
