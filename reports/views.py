from django.http import HttpResponse
import json
from django.shortcuts import render
from patient_opd.models import PatientOpdModel

from reports.report_sync import download_report
from django.views.decorators.csrf import csrf_exempt
from .rpt.usg_report_rpt import usg_rpt
from .rpt.consultation_rpt import consultation_rpt
from .rpt.birth_rpt import birth_rpt
from .rpt.delivery_rpt import delivery_rpt
from .rpt.billing_rpt import billing_rpt
from .rpt.discharge_rpt import discharge_rpt
from .rpt.mtp_list_rpt import mtp_list_rpt
from .rpt.referal_slip_rpt import referal_slip_rpt
from patient_delivery.models import PatientDeliveryModel
from django.db.models import Count
from datetime import datetime
from django.db.models.functions import TruncMonth,TruncYear,ExtractMonth
from django.db.models import Count

from patient.models import PatientModel
from django.db.models import Q
from user.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def usg_report(request, id, language_id=None):
    return usg_rpt(request, id, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def consultation_report(request, id, language_id=None):
    return consultation_rpt(request, id, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def discharge_report(request, id, language_id=None):
    return discharge_rpt(request, id, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def birth_report(request, id, language_id=None):
    return birth_rpt(request, id, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delivery_report(request, language_id=None):
    data = request.query_params
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    ids = data.get("ids",None)
    return delivery_rpt(request, start_date, end_date, ids, language_id)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def billing_report(request,language_id=None):
    data = request.query_params
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)

    return billing_rpt(request, start_date, end_date, language_id)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mtp_list_report(request, language_id=None):
    return mtp_list_rpt(request, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def referal_slip_report(request, id, language_id=None):
    return referal_slip_rpt(request, id, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def download_pdf_report(request, report_name, id, language_id=None):
    url = "/report/" + report_name + "/" + str(id) + "/" + str(language_id)
    return download_report(request, url, "usg_report.pdf", "A4", "Potrait")


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_report(request, id, language_id=None):
    template_name = "reports/en/report-3.html"
    return render(request, template_name)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def match_regd_no(request):
    user_list = User.objects.filter(
        Q(phone__icontains="F") | Q(phone__exact=0) | Q(phone__exact="")
    )

    for user in user_list:
        patient_list = PatientModel.objects.filter(id=user.id)

        for patient in patient_list:
            print(patient.registered_no, "====", patient.phone)

            patient.phone = "F_" + str(patient.registered_no)
            patient.save()

    return HttpResponse("data")


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def active_patient(request, id=None):

    patient = PatientModel.objects.filter(deleted=0)
    if id:
        patient = patient.filter(created_by=id)
    active_patient = len(patient)

    ob_count = patient.filter(consultationmodel__patient_type="OB",created_at__date__month=datetime.now().month).count()
    gyn_count = patient.filter(consultationmodel__patient_type="GYN",created_at__date__month=datetime.now().month).count()

    patient_opd = PatientOpdModel.objects.filter(deleted=0)
    if id:
        patient_opd = patient_opd.filter(created_by=id)

    opd_count = len(patient_opd)

    today_patiend_opd = patient_opd.filter(created_at__date=datetime.now())
    today_opd_count = len(today_patiend_opd)

    month_patiend_opd = patient_opd.filter(created_at__date__month=datetime.now().month)
    month_opd_count = len(month_patiend_opd)

    delivery_report = (
        PatientDeliveryModel.objects.filter(
             deleted=0,created_at__date__year=datetime.now().year
        )
        .annotate(Month=ExtractMonth("created_at"))
        .values("Month")
        .annotate(Delivery=Count("patient_delivery_id"))
        .values("Month", "Delivery")
    )

    monthly_opd_report = (
        PatientOpdModel.objects.filter(
             deleted=0,created_at__date__year=datetime.now().year
        )
        .annotate(Month=ExtractMonth("created_at"))
        .values("Month")
        .annotate(Delivery=Count("patient_opd_id"))
        .values("Month", "Delivery")
    )

    if len(list(delivery_report))>0:
        delivery_report = list(delivery_report)
    else:
        delivery_report[0]=0

    data = {}
    data["active_patient"] = active_patient
    data["opd_count"] = opd_count
    data["today_opd_count"] = today_opd_count
    data["month_opd_count"] = month_opd_count
    data["monthly_delivery"] = list(delivery_report)
    data["monthly_opd_graph"]= list(monthly_opd_report)
    data["ob_count"] = ob_count
    data["gyn_count"] = gyn_count

    return HttpResponse(json.dumps(data))
