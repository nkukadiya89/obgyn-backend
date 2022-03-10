from django.shortcuts import render, HttpResponse
from rest_framework import status

from patient_opd.models import PatientOpdModel
from reports.report_sync import download_report
from template_header.models import TemplateHeaderModel


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


def consultation_report(request, id, language_id=None):
    patient_opd = PatientOpdModel.objects.filter(pk=id).select_related('consultationmodel')

    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1).first()

    patient_opd = patient_opd.first()
    if patient_opd == None:
        return HttpResponse("Record Does not exist", status=status.HTTP_400_BAD_REQUEST)
    context = {}
    context["receipt_date"] = str(patient_opd.opd_date)
    context["regd_no"] = patient_opd.patient.registered_no
    context["name"] = "".join(
        [patient_opd.patient.first_name, " ", patient_opd.patient.middle_name, " ", patient_opd.patient.last_name])
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


def discharge_report(request, id, language_id=None):
    template_name = "reports/en/discharge_card.html"
    return render(request, template_name)


def birth_report(request, id, language_id=None):
    template_name = "reports/en/birth_report.html"
    return render(request, template_name)


def mtp_list_report(request, id, language_id=None):
    template_name = "reports/en/mtp_list.html"
    return render(request, template_name)


def referal_slip_report(request, id, language_id=None):
    template_name = "reports/en/referal_slip.html"
    return render(request, template_name)


def download_pdf_report(request, report_name, id, language_id=None):
    url = "/report/" + report_name + "/" + str(id) + "/" + str(language_id)
    return download_report(request, url, "usg_report.pdf", "A4", "Potrait")


def view_report(request, id, language_id=None):
    template_name = "reports/en/report-3.html"
    return render(request, template_name)
