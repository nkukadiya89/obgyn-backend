import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.db.models import Q

from utility.search_filter import filtering_query
from .models import ObgynConfigModel
from .serializers import Obgyn_Configserializers
from utility.decorator import validate_permission, validate_permission_id


from django.shortcuts import render
from user.models import User
from financial_year.models import FinancialYearModel
from django.utils.timezone import now
from patient_usgform.models import PatientUSGFormModel
from obgyn_config.models import ObgynConfigModel
from datetime import date
import calendar 
from django.utils.timezone import now

# Create your views here.


def update_obgyn_config(request):
    user = User.objects.filter(id=request.data.get("user"), user_type="DOCTOR").first()

    if user:
        fy = (
            FinancialYearModel.objects.filter(
                start_date__lte=now(), end_date__gte=now()
            )
            .values_list("fid")
            .first()
        )

        start_date = fy.start_date
        end_date = fy.end_date

        obgyn_config = ObgynConfigModel.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            user_id=user.id
        )

        month = date.today().month
        year = date.today().year
        _, num_days = calendar.monthrange(2016, 3)
        first_date = date(year, month, 1)
        last_date = date(year, month, num_days)

        usg_form_y = PatientUSGFormModel.objects.filter(deleted=0,created_at__date__gte=start_date,
            created_at__date__lte=end_date, created_by=user.id)

        usg_form_m =PatientUSGFormModel.objects.filter(deleted=0,created_at__date__gte=first_date,
            created_at__date__lte=last_date, created_by=user.id)
 
        if obgyn_config == None:
            obgyn_config = ObgynConfigModel.objects.create(user_id=user.id,created_by=user.id,deleted=0)
        
        if usg_form_y == None:
            obgyn_config.monthly_usg = 1
            obgyn_config.yearly_usg = 1
        else:
            obgyn_config.yearly_usg = len(usg_form_y) + 1
            if usg_form_m == None:
                obgyn_config.monthly_usg = 1
            else:
                obgyn_config.monthly_usg = len(usg_form_m) + 1
        
        obgyn_config.save()


def get_obgyn_config(user):
    month_seq = 0
    year_seq = 0

    fy =FinancialYearModel.objects.filter(
            start_date__lte=now(), end_date__gte=now()
        ).first()
    
    start_date = fy.start_date
    end_date = fy.end_date
    
    month = date.today().month
    year = date.today().year
    _, num_days = calendar.monthrange(2016, 3)
    first_date = date(year, month, 1)
    last_date = date(year, month, num_days)

    usg_form_y = PatientUSGFormModel.objects.filter(deleted=0,created_at__date__gte=start_date,
            created_at__date__lte=end_date, created_by=user.id)
    
    print(len(usg_form_y))

    usg_form_m =PatientUSGFormModel.objects.filter(deleted=0,created_at__date__gte=first_date,
        created_at__date__lte=last_date, created_by=user.id)

    if usg_form_y == None:
        month_seq = 1
        year_seq = 1
    else:
        year_seq = len(usg_form_y) + 1
        if usg_form_m == None:
            month_seq = 1
        else:
            month_seq = len(usg_form_m) + 1

    return month_seq, year_seq

def update_global_charges(request):
    user = request.user
    obgyn_config = ObgynConfigModel.objects.filter(user_id=user.id).first()

    if obgyn_config == None:
        obgyn_config = ObgynConfigModel.objects.create(user_id=user.id,deleted=0)

    

    if "rs_per_visit" in request.data:
        obgyn_config.rs_per_visit = request.data.get("rs_per_visit",0)
    if "rs_per_usg" in request.data:
        obgyn_config.rs_per_usg = request.data.get("rs_per_usg",0)
    if "rs_per_room" in request.data:
        obgyn_config.rs_per_room = request.data.get("rs_per_room",0)
    if "operative_charge" in request.data:
        obgyn_config.operative_charge = request.data.get("operative_charge",0)
    if "rs_per_day_nursing" in request.data:
        obgyn_config.rs_per_day_nursing = request.data.get("rs_per_day_nursing",0)
    
    obgyn_config.save()

class ObgynConfigAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            obgyn_config = ObgynConfigModel.objects.filter(pk=id).first()
        except ObgynConfigModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = Obgyn_Configserializers(obgyn_config, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Create New Record=========================
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("obgyn_config","add")
def create(request):
    data = {}
    if request.method == "POST":
        obgyn_config = ObgynConfigModel()
        serializer = Obgyn_Configserializers(obgyn_config, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("obgyn_config","change")
def patch(request, id):
    data = {}
    try:
        if id:
            obgyn_config = ObgynConfigModel.objects.get(pk=id)
        else:
            obgyn_config = ObgynConfigModel.objects.filter(deleted=0)
    except ObgynConfigModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = Obgyn_Configserializers(obgyn_config, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


# ================= Retrieve Single or Multiple records=========================
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("obgyn_config","view")
def get(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            obgyn_config = ObgynConfigModel.objects.filter(pk=id, deleted=0)
        else:
            obgyn_config = ObgynConfigModel.objects.filter(Q(created_by=1,deleted=0) | Q(created_by=request.data.get('created_by')))

        data["total_record"] = len(obgyn_config)

        obgyn_config, data = filtering_query(
            obgyn_config, query_string, "obgyn_config_id", "OBGYNCONFIG")

    except ObgynConfigModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = Obgyn_Configserializers(obgyn_config, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

