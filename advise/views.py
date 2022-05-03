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
from .models import AdviseModel
from .serializers import AdviseSerializers
from utility.decorator import validate_permission


class AdviseAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["advise_name"]


    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            advise = AdviseModel.objects.filter(pk=id).first()
        except AdviseModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = AdviseSerializers(advise, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("advise","change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))

    if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
            advise = AdviseModel.objects.filter(advise_id__in=del_id["id"])
    except AdviseModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = advise.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("advise","add")
def post(request):
    data = {}
    if request.method == "POST":
            advise = AdviseModel()
            serializer = AdviseSerializers(advise, data=request.data)

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
@validate_permission("advise","change")
def patch(request, id):
    data = {}
    try:
        if id:
            advise = AdviseModel.objects.get(pk=id)
        else:
            advise = AdviseModel.objects.filter(deleted=0)
    except AdviseModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = AdviseSerializers(advise, request.data, partial=True)

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
@validate_permission("advise","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data={}
    try:
        if id:
            advise = AdviseModel.objects.filter(pk=id, deleted=0)
        else:
            advise = AdviseModel.objects.filter(deleted=0)

        data["total_record"] = len(advise)
        advise, data = filtering_query(advise, query_string, "advise_id", "ADVISE")

    except AdviseModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = AdviseSerializers(advise, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
