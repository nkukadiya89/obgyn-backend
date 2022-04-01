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
from .models import SurgicalItemModel, SurgicalItemGroupModel
from .serializers import SurgicalItemSerializers, SurgicalItemGroupSerializers


class SurgicalItemAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            surgical_item = SurgicalItemModel.objects.filter(pk=id).first()
        except SurgicalItemModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = SurgicalItemSerializers(surgical_item, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))
        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            surgical_item = SurgicalItemModel.objects.filter(surgical_item_id__in=del_id["id"])
        except SurgicalItemModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = surgical_item.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            surgical_item = SurgicalItemModel()
            serializer = SurgicalItemSerializers(surgical_item, data=request.data)

            if serializer.is_valid():
                serializer.save()

                if "surgical_item_group_name" in request.data:
                    surgical_item_group_name = str(request.data.get('surgical_item_group_name')).strip()
                    surgical_item_group = SurgicalItemGroupModel.objects.filter(
                        drug_group_name=surgical_item_group_name).first()
                    
                    if surgical_item_group == None:
                        surgical_item_group = SurgicalItemGroupModel.objects.create(
                            drug_group_name=surgical_item_group_name,
                            created_by=request.data.get('created_by'),
                            deleted=0)
                    surgical_item_group.surgical_item.add(surgical_item.surgical_item_id)

                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_201_CREATED)

            data["success"] = False
            data["msg"] = serializer.errors
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class SurgicalItemGroupAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(pk=id).first()
        except SurgicalItemGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = SurgicalItemGroupSerializers(surgical_item_group, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))
        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(si_group_id__in=del_id["id"])
        except SurgicalItemGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = surgical_item_group.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            surgical_item_group = SurgicalItemGroupModel()
            serializer = SurgicalItemGroupSerializers(surgical_item_group, data=request.data)

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
@permission_classes([IsAuthenticated])
def patch_surgical_group(request, id):
    data = {}

    try:
        if id:
            surgical_item_group = SurgicalItemGroupModel.objects.get(pk=id)
        else:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(deleted=0)
    except SurgicalItemGroupModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = SurgicalItemGroupSerializers(surgical_item_group, request.data, partial=True)

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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def patch(request, id):
    data = {}

    try:
        if id:
            surgical_item = SurgicalItemModel.objects.get(pk=id)
        else:
            surgical_item = SurgicalItemModel.objects.filter(deleted=0)
    except SurgicalItemModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = SurgicalItemSerializers(surgical_item, request.data, partial=True)

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
@permission_classes([IsAuthenticated])
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            surgical_item = SurgicalItemModel.objects.filter(pk=id, deleted=0)
        else:
            surgical_item = SurgicalItemModel.objects.filter(deleted=0)

        data["total_record"] = len(surgical_item)
        surgical_item, data = filtering_query(surgical_item, query_string, "surgical_item_id", "SURGICALITEM")

    except SurgicalItemModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = SurgicalItemSerializers(surgical_item, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
# ================= Retrieve Single or Multiple records=========================
def get_group(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(pk=id, deleted=0)
        else:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(deleted=0)

            data["total_record"] = len(surgical_item_group)
            surgical_item_group, data = filtering_query(surgical_item_group, query_string, "si_group_id",
                                                        "SURGICALITEMGROUP")

    except SurgicalItemGroupModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = SurgicalItemGroupSerializers(surgical_item_group, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
