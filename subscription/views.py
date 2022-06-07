import json

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import SubscriptionModel
from .serializers import SubscriptionSerializers
from utility.search_filter import filtering_query
from utility.decorator import validate_permission, validate_permission_id


class SubscriptionAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Delete Record =========================
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@validate_permission("subscription","change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        subscription = SubscriptionModel.objects.filter(
            subscription_id__in=del_id["id"])
    except SubscriptionModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = subscription.delete()
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("subscription","add")
def create(request):
    print(request.data)
    data = {}
    if request.method == "POST":
        subscription = SubscriptionModel()
        serializer = SubscriptionSerializers(subscription, data=request.data)

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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("subscription","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data={}
    try:
        if id:
            subscription = SubscriptionModel.objects.filter(pk=id, deleted=0)
        else:
            subscription = SubscriptionModel.objects.filter(deleted=0)

        data["total_record"] = len(subscription)
        subscription, data = filtering_query(subscription, query_string, "subscription_id", "SUBSCRIPTION")

    except SubscriptionModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = SubscriptionSerializers(subscription, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
