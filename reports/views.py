from django.shortcuts import render

from reports.report_sync import download_report
from django.views.decorators.csrf import csrf_exempt
from .rpt.usg_report_rpt import usg_rpt
from .rpt.consultation_rpt import consultation_rpt
from .rpt.birth_rpt import birth_rpt
from .rpt.discharge_rpt import discharge_rpt
from .rpt.mtp_list_rpt import mtp_list_rpt
from .rpt.referal_slip_rpt import referal_slip_rpt


@csrf_exempt
def usg_report(request, id, language_id=None):
    return usg_rpt(request, id, language_id)


@csrf_exempt
def consultation_report(request, id, language_id=None):
    return consultation_rpt(request, id, language_id)

@csrf_exempt
def discharge_report(request, id, language_id=None):
    return discharge_rpt(request, id, language_id)


@csrf_exempt
def birth_report(request, id, language_id=None):
    return birth_rpt(request, id, language_id)

@csrf_exempt
def mtp_list_report(request, id, language_id=None):
    return mtp_list_rpt(request, id, language_id)

@csrf_exempt
def referal_slip_report(request, id, language_id=None):
    return referal_slip_rpt(request, id, language_id)


@csrf_exempt
def download_pdf_report(request, report_name, id, language_id=None):
    url = "/report/" + report_name + "/" + str(id) + "/" + str(language_id)
    return download_report(request, url, "usg_report.pdf", "A4", "Potrait")


@csrf_exempt
def view_report(request, id, language_id=None):
    template_name = "reports/en/report-3.html"
    return render(request, template_name)
