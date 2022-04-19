from django.shortcuts import render, HttpResponse
from rest_framework import status

from patient.models import PatientModel
from patient_delivery.models import PatientDeliveryModel
from patient_mtp.models import PatientMtpModel
from patient_opd.models import PatientOpdModel
from reports.report_sync import download_report
from template_header.models import TemplateHeaderModel
from consultation.models import ConsultationModel
from language.models import LanguageModel
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def usg_report(request, id, language_id=None):
    patient_opd = PatientOpdModel.objects.filter(pk=id).select_related('consultationmodel')

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()

    patient_opd = patient_opd.first()
    if patient_opd == None:
        return HttpResponse("Record Does not exist", status=status.HTTP_400_BAD_REQUEST)

    template_name = "reports/en/usg_report.html"
    context = {}
    context["receipt_date"] = str(patient_opd.opd_date)
    context["regd_no"] = patient_opd.patient.registered_no
    context["hb"] = ""
    context["name"] = "".join(
        [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
    context["mobile_no"] = patient_opd.patient.phone
    context["blood_group"] = patient_opd.consultationmodel.hb
    context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                  patient_opd.patient.district.district_name, " ",
                                  patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])
    context["report_date"] = str(patient_opd.opd_date)
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})


@csrf_exempt
def consultation_report(request, id, language_id=None):
    
    consultation = ConsultationModel.objects.filter(pk=id).first()
    if consultation == None:
        return HttpResponse("Consultation Record Does not exist", status=status.HTTP_400_BAD_REQUEST)

    language = LanguageModel.objects.filter(pk=language_id).first()

    if language == None:
        return HttpResponse("Invalid Language selected", status=status.HTTP_400_BAD_REQUEST)

    patient_opd = PatientOpdModel.objects.filter(pk=id).select_related('consultationmodel')


    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()

    

    patient_opd = patient_opd.first()
    if patient_opd == None:
        return HttpResponse("OPD Record Does not exist", status=status.HTTP_400_BAD_REQUEST)
        
    context = {}
    context["receipt_date"] = str(patient_opd.opd_date)
    context["regd_no"] = patient_opd.patient.registered_no
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


@csrf_exempt
def discharge_report(request, id, language_id=None):
    patient_opd = PatientOpdModel.objects.filter(pk=id).select_related('patientdischargemodel').first()
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()
    context = {}
    context["name"] = "".join(
        [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
    context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                  patient_opd.patient.district.district_name, " ",
                                  patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])

    context["admission_date"] = str(patient_opd.patientdischargemodel.admission_date) + " " + str(
        patient_opd.patientdischargemodel.admission_time)
    context["discharge_date"] = str(patient_opd.patientdischargemodel.discharge_date) + " " + str(
        patient_opd.patientdischargemodel.discharge_time)
    context["complain_of"] = patient_opd.patientdischargemodel.complain_of
    context["diagnosis"] = patient_opd.patientdischargemodel.diagnosis.diagnosis_name
    context["ot_time_date"] = str(patient_opd.patientdischargemodel.ot_date) + " " + str(
        patient_opd.patientdischargemodel.ot_time)
    context["treatment_given"] = patient_opd.patientdischargemodel.treatment_given
    context["advice"] = patient_opd.patientdischargemodel.advice.field_value
    context["remark"] = patient_opd.patientdischargemodel.remark
    context["name_of_procedure"] = patient_opd.patientdischargemodel.name_of_operation
    template_name = "reports/en/discharge_card.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})


@csrf_exempt
def birth_report(request, id, language_id=None):
    patient = PatientModel.objects.filter(pk=id).first()
    patient_delivery = PatientDeliveryModel.objects.filter(patient=patient).first()
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()
    context = {}

    context["mother_name"] = "".join(
        [patient.first_name, " ", patient.middle_name, " ", patient.last_name])
    context["father_name"] = patient_delivery.husband_name
    context["address"] = "".join([" ", patient.city.city_name, " ",
                                  patient.district.district_name, " ",
                                  patient.taluka.taluka_name, " ", patient.state.state_name])
    context["age"] = patient.age
    context["date"] = patient_delivery.birth_date
    context["time"] = patient_delivery.birth_time
    context["gender"] = patient_delivery.child_gender
    context["weight"] = patient_delivery.weight
    context["child_status"] = patient_delivery.baby_status
    context["child_count"] = patient_delivery.live_male_female
    context["episitomy_by"] = patient_delivery.weight

    template_name = "reports/en/birth_report.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})


@csrf_exempt
def mtp_list_report(request, id, language_id=None):
    from_date = request.body.get('from_date')
    to_date = request.body.get('to_date')

    patient_mtp_list = PatientMtpModel.objects.all()


    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()

    context_list=[]
    for patient_mtp in patient_mtp_list:
        patient_opd_id=patient_mtp.patient_opd_id
        patient_opd = PatientOpdModel.objects.filter(pk=patient_opd_id).select_related('patientdischargemodel').first()

        context = {}
        context["date_of_admission"] = patient_opd.patientdischargemodel.admission_date
        context["name"] = "".join(
            [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
        context["husband_name"] = patient_opd.patient.husband_father_name
        context["age"] = patient_opd.patient.age
        context["religion"] = patient_opd.patient.religion
        context["address"] = "".join([" ", patient_opd.patient.city.city_name, " ",
                                      patient_opd.patient.district.district_name, " ",
                                      patient_opd.patient.taluka.taluka_name, " ", patient_opd.patient.state.state_name])
        context["duration"] = "pending"
        context["reason"] = patient_mtp.reason_for_mtp
        context["termination_date"] = patient_mtp.termination_date
        context["discharge_date"] = patient_mtp.discharge_date
        context["remark"] = patient_mtp.remark
        context["opinion_by_name"] = "fix to be changed"
        context["terminated_by"] = "fix to be changed"
        context_list.append(context)
    template_name = "reports/en/mtp_list.html"
    return render(request, template_name,
                  {"context_list": context_list, "template_header": template_header.header_text.replace("'", "\"")})


@csrf_exempt
def referal_slip_report(request, id, language_id=None):
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()

    context = {}

    template_name = "reports/en/referal_slip.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})


@csrf_exempt
def download_pdf_report(request, report_name, id, language_id=None):
    url = "/report/" + report_name + "/" + str(id) + "/" + str(language_id)
    return download_report(request, url, "usg_report.pdf", "A4", "Potrait")


@csrf_exempt
def view_report(request, id, language_id=None):
    template_name = "reports/en/report-3.html"
    return render(request, template_name)
