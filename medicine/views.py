import json

from django.db.models import Q
from django.db.models.functions import Lower
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from utility.decorator import validate_permission, validate_permission_id
from utility.search_filter import filtering_query
from .models import MedicineModel, TimingModel, MedicineTypeModel
from .serializers import (
    MedicineSerializers,
    MedicineTypeSerializers,
    TimingSerializers,
    DynamicFieldModelSerializer,
)
from .utils_view import link_diagnosis, delete_child_table


class MedicineAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            medicine = MedicineModel.objects.filter(pk=id).first()
        except MedicineModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = MedicineSerializers(medicine, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= Delete Record =========================
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("medicine", "change")
def delete_medicine(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        medicine = MedicineModel.objects.filter(medicine_id__in=del_id["id"])
    except MedicineModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        delete_child_table(del_id["id"])
        result = medicine.delete()
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Create New Record=========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("medicine", "add")
def create_medicine(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        medicine = MedicineModel()
        serializer = MedicineSerializers(medicine, data=request.data)

        if serializer.is_valid():
            serializer.save()

            data["msg"] = "Data updated successfully"

            if "diagnosis_name" in request.data and "diagnosis_type" in request.data:
                if not link_diagnosis(request, serializer.data["medicine_id"]):
                    data[
                        "msg"
                    ] = "Medicine Created successfully but not linked with Diagnosis"
            if (
                    "diagnosis_name" in request.data
                    and "diagnosis_type" not in request.data
            ):
                data[
                    "msg"
                ] = "Medicine Created successfully but not linked with Diagnosis"

            data["success"] = True

            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class MedicineTypeAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            medicine_type = MedicineTypeModel.objects.filter(pk=id).first()
        except MedicineTypeModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = MedicineTypeSerializers(medicine_type, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= Delete Record =========================
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("medicine_type", "delete")
def delete_medicine_type(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    try:
        medicine_type = MedicineTypeModel.objects.filter(
            medicine_type_id__in=del_id["id"]
        )
    except MedicineTypeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = medicine_type.delete()
        # DiagnosisMedicineModel.objects.filter(medicine_type_id__in=del_id["id"]).delete()
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Create New Record=========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("medicine_type", "add")
def create_medicine_type(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        medicine_type = MedicineTypeModel()
        serializer = MedicineTypeSerializers(medicine_type, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class TimingAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            timing = TimingModel.objects.filter(pk=id).first()
        except TimingModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = TimingSerializers(timing, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= Delete Record =========================
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("timing", "change")
def delete_timing(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        timing = TimingModel.objects.filter(timing_id__in=del_id["id"])
    except TimingModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = timing.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Create New Record=========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("timing", "add")
def create_timing(request):
    data = {}
    request.data["created_by"] = request.user.id
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        timing = TimingModel()
        serializer = TimingSerializers(timing, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


# ================= Retrieve Single or Multiple records=========================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("timing", "view")
def get_timing(request, id=None):
    data = {}
    query_string = request.query_params

    adminRecord = True
    if "adminRecord" in query_string:
        adminRecord = True if query_string["adminRecord"] == "true" else False

    try:
        if id:
            timing = TimingModel.objects.filter(pk=id, deleted=0)
        else:
            if adminRecord:
                timing = TimingModel.objects.filter(
                    Q(deleted=0, created_by=1)
                    | Q(created_by=request.user.id, deleted=0)
                )
            else:
                timing = TimingModel.objects.filter(
                    created_by=request.user.id, deleted=0
                )

        data["total_record"] = len(timing)
        timing, data = filtering_query(timing, query_string, "timing_id", "TIMING")

    except TimingModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = TimingSerializers(timing, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("timing", "change")
def patch_timing(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            timing = TimingModel.objects.get(pk=id, deleted=0)
        else:
            timing = TimingModel.objects.filter(deleted=0)
    except TimingModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = TimingSerializers(timing, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("medicine_type", "update")
def patch_medicine_type(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            medicine_type = MedicineTypeModel.objects.get(pk=id, deleted=0)
        else:
            medicine_type = MedicineTypeModel.objects.filter(deleted=0)
    except MedicineTypeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = MedicineTypeSerializers(medicine_type, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("medicine", "change")
def patch_medicine(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            medicine = MedicineModel.objects.get(pk=id, deleted=0)
        else:
            medicine = MedicineModel.objects.filter(deleted=0)
    except MedicineModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = MedicineSerializers(medicine, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            if "diagnosis_name" in request.data and "diagnosis_type" in request.data:
                status_flag = link_diagnosis(request, serializer.data["medicine_id"])

            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


# ================= Retrieve Single or Multiple records=========================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("medicine", "view")
def get_medicine(request, id=None):
    query_string = request.query_params

    adminRecord = True
    if "adminRecord" in query_string:
        adminRecord = True if query_string["adminRecord"] == "true" else False

    data = {}
    try:
        if id:
            medicine = MedicineModel.objects.filter(pk=id, deleted=0)
        else:
            if adminRecord:
                medicine = MedicineModel.objects.filter(
                    Q(deleted=0, created_by=1)
                    | Q(created_by=request.user.id)
                )
            else:
                medicine = MedicineModel.objects.filter(
                    created_by=request.user.id, deleted=0
                )

        data["total_record"] = len(medicine)

        medicine, data = filtering_query(
            medicine, query_string, "medicine_id", "MEDICINE"
        )

    except MedicineModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = MedicineSerializers(medicine, many=True)
        if "fields" in query_string:
            if query_string["fields"]:
                serializer = DynamicFieldModelSerializer(
                    medicine, many=True, fields=query_string["fields"]
                )

        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Retrieve Single or Multiple records=========================


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("medicine", "view")
# ================= Retrieve Single or Multiple records=========================
def get_or_medicine(request, id=None):
    query_string = request.query_params

    adminRecord = False
    if "adminRecord" in query_string:
        adminRecord = True if query_string["adminRecord"] == "true" else False

    data = {}
    try:
        if id:
            medicine = MedicineModel.objects.filter(pk=id, deleted=0)
        else:
            if adminRecord:
                medicine = MedicineModel.objects.filter(
                    Q(deleted=0, created_by=1)
                    | Q(created_by=request.user.id)
                )
            else:
                medicine = MedicineModel.objects.filter(
                    created_by=request.user.id, deleted=0
                )

        data["total_record"] = len(medicine)

        medicine, data = filtering_query(
            medicine, query_string, "medicine_id", "MEDICINEOR"
        )

    except MedicineModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = MedicineSerializers(medicine, many=True)
        if "fields" in query_string:
            if query_string["fields"]:
                serializer = DynamicFieldModelSerializer(
                    medicine, many=True, fields=query_string["fields"]
                )

        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Retrieve Single or Multiple records=========================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("medicine_type", "view")
# ================= Retrieve Single or Multiple records=========================
def get_medicine_type(request, id=None):
    query_string = request.query_params

    adminRecord = False
    if "adminRecord" in query_string:
        adminRecord = True if query_string["adminRecord"] == "true" else False

    data = {}
    try:
        if id:
            medicine_type = MedicineTypeModel.objects.filter(pk=id, deleted=0)
        else:
            if adminRecord:
                medicine_type = MedicineTypeModel.objects.filter(
                    Q(deleted=0, created_by=1)
                    | Q(created_by=request.user.id)
                )
            else:
                medicine_type = MedicineTypeModel.objects.filter(
                    created_by=request.user.id, deleted=0
                )

        data["total_record"] = len(medicine_type)
        medicine_type, data = filtering_query(
            medicine_type, query_string, "medicine_type_id", "MEDICINETYPE"
        )

    except MedicineTypeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = MedicineTypeSerializers(medicine_type, many=True)

        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Retrieve Single or Multiple records=========================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("medicine_type", "view")
# ================= Retrieve Single or Multiple records=========================
def get_unique_medicine(request, id=None):
    query_string = request.query_params
    if "," in query_string["fields"]:
        distinc_key = query_string["fields"].split(",")[1]
    else:
        distinc_key = query_string["fields"]

    data = {}
    try:
        if id:
            medicine = MedicineModel.objects.filter(pk=id, deleted=0).order_by(Lower(distinc_key))
        else:
            medicine = MedicineModel.objects.filter(
                Q(deleted=0, created_by=1)
                | Q(created_by=request.user.id)
            )
        data["total_record"] = len(medicine)

        # medicine = medicine.distinct(distinc_key).values_list(distinc_key)
        medicine = medicine.distinct(distinc_key)
    except MedicineModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = DynamicFieldModelSerializer(medicine, many=True, fields=query_string["fields"])

        # medicine = [item for m in medicine for item in m]

        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission("medicine_type", "view")
def medicine_to_type(request):
    data = {}
    query_string = request.query_params
    medicine_name = query_string["medicine_name"]

    medicine_list = list(
        MedicineModel.objects.filter(medicine__iexact=medicine_name).values_list('medicine_type_id', flat=True))

    if medicine_list:
        medicine_type = MedicineTypeModel.objects.filter(medicine_type_id__in=medicine_list).distinct()

    if len(medicine_type) >0:
        serializer = MedicineTypeSerializers(medicine_type, many=True)
    else:
        serializer = MedicineTypeSerializers(MedicineSerializers())

    data["success"] = True
    data["msg"] = "OK"
    data["data"] = serializer.data
    return Response(data=data, status=status.HTTP_200_OK)
