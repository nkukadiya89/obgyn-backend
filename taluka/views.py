import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from utility.search_filter import filtering_query
from .models import TalukaModel
from .serializers import TalukaSerializers
from utility.decorator import validate_permission, validate_permission_id


class TalukaAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["taluka_name"]


    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            taluka = TalukaModel.objects.filter(pk=id).first()
        except TalukaModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = TalukaSerializers(taluka, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Delete Record =========================
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@validate_permission("taluka","change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))

    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        taluka = TalukaModel.objects.filter(taluka_id__in=del_id["id"])
    except TalukaModel:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = taluka.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("taluka","add")
def create(request):
    data = {}
    if request.method == "POST":
        taluka = TalukaModel()
        serializer = TalukaSerializers(taluka, data=request.data)

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
@validate_permission_id("taluka","change")
def patch(request, id):
    data = {}
    try:
        if id:
            taluka = TalukaModel.objects.get(pk=id, deleted=0)
        else:
            taluka = TalukaModel.objects.filter(deleted=0)
    except TalukaModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = TalukaSerializers(taluka, request.data, partial=True)

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

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("taluka","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data={}
    try:
        if id:
            taluka = TalukaModel.objects.filter(pk=id, deleted=0)
        else:
            taluka = TalukaModel.objects.filter(deleted=0)

        data["total_record"] = len(taluka)
        taluka, data = filtering_query(taluka, query_string, "taluka_id", "TALUKA")

    except TalukaModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = TalukaSerializers(taluka, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
