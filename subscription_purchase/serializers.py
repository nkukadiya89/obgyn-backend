from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from .models import Subscription_purchaseModel
import datetime
from .utils_views import generate_invoice_no
from subscription.serializers import SubscriptionSerializers
from user.serializers import UserSerializers


    

class Subscription_PurchaseSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(Subscription_PurchaseSerializers,
                    self).to_representation(instance)

        if instance.hospital.user_type=="HOSPITAL":
            ret["hospital_name"] = UserSerializers(instance.hospital).data["hospital_name"]
        else:
            ret["hospital_name"] = ""

        ret["subscription_name"] = SubscriptionSerializers(instance.subscription).data["subscription_name"]
        return ret

    def validate(self,data):
        start_date = over_date = ""

        if "start_date" in data:
            data["start_date"] = data.get("start_date")
        
        if data["start_date"] == None:
            data["start_date"] = datetime.date.today()
        
        
        if not data["duration"] in data:
            data["duration"] = 365

        if "over_date" in data:
            data["over_date"] = data.get("over_date")
        else:
            data["over_date"] = datetime.date.today() + datetime.timedelta(days=int(data["duration"]))
            

        if data["over_date"] == None:
            data["over_date"] = datetime.date.today()

        data["invoice_no"], data["inv_year"] = generate_invoice_no()
        
        
        return data

        if "hospital" in ret:
            ret["hospital_name"] = UserSerializers(instance.hospital).data["hospital_name"]
            ret["hospital"] = UserSerializers(instance.hospital).data["hospital"]

        if "subscription" in ret:
            ret["subscription_name"] = SubscriptionSerializers(instance.subscription).data["subscription_name"]
            ret["subscription"] = SubscriptionSerializers(instance.subscription).data["subscription_id"]
        return ret

        
    subscription_purchase_id = serializers.IntegerField(read_only=True)
    start_date = serializers.DateField(format="%d-%m-%Y")
    over_date = serializers.DateField(read_only=True,format="%d-%m-%Y")
    invoice_no = serializers.IntegerField(read_only=True)
    inv_year = serializers.CharField(read_only=True)


    class Meta:
        model = Subscription_purchaseModel
        exclude = ("created_at",)
