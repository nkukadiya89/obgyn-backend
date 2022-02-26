from django.shortcuts import render, HttpResponse
from rest_framework import status

from patient_opd.models import PatientOpdModel


def view_report(request, id):
    patient_opd = PatientOpdModel.objects.filter(pk=id).select_related('consultationmodel')

    patient_opd = patient_opd.first()
    if patient_opd == None:
        data = {}
        # data["success"] = False
        # data["msg"] = "Record Does not exist"
        # data["data"] = []
        return HttpResponse("Record Does not exist", status=status.HTTP_400_BAD_REQUEST)

    template_name = "reports/en/report-1.html"
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
    return render(request, template_name, {"context": context})
