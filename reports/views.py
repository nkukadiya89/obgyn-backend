from django.http import HttpResponse
import json
from django.shortcuts import render
import language
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
from .rpt.daily_opd_income import daily_opd_income_rpt
from .rpt.hospital_bill_rpt import hospital_bill_rpt
from .rpt.indoor_case_paper_rpt import indoor_case_paper_rpt
from .rpt.indoor_case_rpt import indoor_case_rpt
from .rpt.medicine_prescription_rpt import medicine_prescription_rpt
from .rpt.medicine_bill import medicine_bill_rpt
from .rpt.monthly_income_rpt import monthly_income_rpt
from .rpt.ovulation_profile_rpt import ovulation_profile_rpt
from .rpt.bill_receipt_rpt import bill_receipt_rpt
from .rpt.usg_list_report_rpt import usg_list_report_rpt
from .rpt.usg_form_report_rpt import usg_form_report_rpt
from patient_delivery.models import PatientDeliveryModel
from django.db.models import Count
from datetime import datetime,date
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
    if start_date:
        start_date = datetime.strptime(start_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    end_date = data.get("end_date", None)
    if end_date:
        end_date = datetime.strptime(end_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    ids = data.get("ids",None)
    return delivery_rpt(request, start_date, end_date, ids, language_id)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def billing_report(request,language_id=None):
    data = request.query_params
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    if start_date:
        start_date = datetime.strptime(start_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    end_date = data.get("end_date", None)
    if end_date:
        end_date = datetime.strptime(end_date,"%d-%m-%Y").strftime("%Y-%m-%d")

    return billing_rpt(request, start_date, end_date, language_id)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mtp_list_report(request, language_id=None):
    data = request.query_params
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    if start_date:
        start_date = datetime.strptime(start_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    end_date = data.get("end_date", None)
    if end_date:
        end_date = datetime.strptime(end_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    return mtp_list_rpt(request, start_date,end_date,language_id)


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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def daily_opd_income(request,language_id):
    data = request.query_params
    rpt_date = data.get("rpt_date",date.today().strftime("%d-%m-%Y") )
    rpt_date = datetime.strptime(rpt_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    
    return daily_opd_income_rpt(request, rpt_date, language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def hospital_bill(request,language_id,bill_no):
    return hospital_bill_rpt(request,bill_no,language_id)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def indoor_case_paper(request,language_id,indoor_no):
    return indoor_case_paper_rpt(request,indoor_no,language_id)    
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def indoor_case(request,language_id,opd_id):
    return indoor_case_rpt(request,opd_id,language_id)    


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def medicine_prescription(request,language_id,voucher_id):
    return medicine_prescription_rpt(request,voucher_id,language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def medicine_bill(request,language_id,voucher_id):
    return medicine_bill_rpt(request,voucher_id,language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def monthly_income(request,language_id):
    data = request.query_params
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    if start_date:
        start_date = datetime.strptime(start_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    end_date = data.get("end_date", None)
    if end_date:
        end_date = datetime.strptime(end_date,"%d-%m-%Y").strftime("%Y-%m-%d")

    return monthly_income_rpt(request,language_id,start_date,end_date)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ovulation_profile(request,language_id,ovulation_id):
    return ovulation_profile_rpt(request,ovulation_id,language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bill_receipt(request,language_id,bill_id):
    return bill_receipt_rpt(request,bill_id,language_id)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def usg_list_report(request,language_id):
    data = request.query_params
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    if start_date:
        start_date = datetime.strptime(start_date,"%d-%m-%Y").strftime("%Y-%m-%d")
    end_date = data.get("end_date", None)
    if end_date:
        end_date = datetime.strptime(end_date,"%d-%m-%Y").strftime("%Y-%m-%d")

    return usg_list_report_rpt(request,language_id,start_date,end_date)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def usg_form_report(request,language_id,usgform_id):
    return usg_form_report_rpt(request,usgform_id,language_id)