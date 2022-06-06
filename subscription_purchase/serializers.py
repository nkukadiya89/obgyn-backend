from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from .models import Subscription_purchaseModel



    

class Subscription_PurchaseSerializers(serializers.ModelSerializer):
    # def to_representation(self, instance):
    #     ret = super(Subscription_PurchaseSerializers, self).to_representation(instance)
    #     ret["start_date"] = instance.start_date.strftime(format="%d-%m-%Y")
    #     ret["over_date"] = instance.over_date.strftime(format="%d-%m-%Y")

    subscription_purchase_id = serializers.IntegerField(read_only=True)
    subscription_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    start_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    over_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    class Meta:
        model = Subscription_purchaseModel
        fields = ['subscription_purchase_id', 'subscription_date', 'hospital', 'subscription', 'price', 'duration',
                  'start_date', 'over_date', 'description', 'inactive', 'tax_perc', 'invoice_no', 'inv_year','created_by','deleted']