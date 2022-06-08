from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from .models import Subscription_purchaseModel
from user.serializers import UserSerializers
from subscription.serializers import SubscriptionSerializers

    

class Subscription_PurchaseSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(Subscription_PurchaseSerializers, self).to_representation(instance)

        if "hospital" in ret:
            ret["hospital_name"] = UserSerializers(instance.hospital).data["hospital_name"]
            ret["hospital"] = UserSerializers(instance.hospital).data["hospital"]

        if "subscription" in ret:
            ret["subscription_name"] = SubscriptionSerializers(instance.subscription).data["subscription_name"]
            ret["subscription"] = SubscriptionSerializers(instance.subscription).data["subscription_id"]
        return ret

        
    subscription_purchase_id = serializers.IntegerField(read_only=True)
    subscription_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    start_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    over_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    class Meta:
        model = Subscription_purchaseModel
        fields = ['subscription_purchase_id', 'subscription_date', 'hospital', 'subscription', 'price', 'duration',
                  'start_date', 'over_date', 'description', 'inactive', 'tax_perc', 'invoice_no', 'inv_year','created_by','deleted']


