from rest_framework import serializers

from patient_opd.models import PatientOpdModel
from patient.models import PatientModel
from .models import PatientBillingModel
from patient_opd.serializers import PatientOpdSerializers
from manage_fields.serializers import ManageFieldsSerializers
from diagnosis.serializers import DiagnosisSerializers


class PatientBillingSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientBillingSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            ret["is_paid"] = PatientOpdSerializers(instance.patient_opd).data["is_paid"]
            ret["first_name"] = PatientOpdSerializers(instance.patient_opd).data["first_name"]
            ret["middle_name"] = PatientOpdSerializers(instance.patient_opd).data["middle_name"]
            ret["last_name"] = PatientOpdSerializers(instance.patient_opd).data["last_name"]
            del ret["patient_opd"]


        for fld_nm in ["procedure_name", "room_type", "other_charge"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data[
                    "field_value"
                ]

        if "diagnosis" in ret:
            ret["diagnosis_name"] = DiagnosisSerializers(instance.diagnosis).data["diagnosis_name"]

        return ret

    def generate_invoice_no(self):
        invoice_no = "new No"
        return invoice_no

    def validate(self, data):

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")
            
        data["consulting_fees"] = float(data["rs_per_visit"]) * int(data["no_of_visit"])
        data["usg_rs"] = float(data["rs_per_usg"]) * int(data["no_of_usg"])
        data["room_rs"] = float(data["rs_per_room"]) * int(data["room_no_of_day"])
        data["nursing_rs"] = float(data["rs_per_day"]) * int(data["nursing_no_of_days"])
        data["payment"] = data["payment"].upper()
        data["total_rs"] = float(data["consulting_fees"]) + float(data["usg_rs"]) + \
                           float(data["room_rs"]) + float(data["procedure_charge"]) + float(
            data["medicine_rs"]) + float(data["nursing_rs"]) + float(data["other_rs"])

        if not self.partial:
            data["invoice_no"] = self.generate_invoice_no()
        return data

    patient_billing_id = serializers.IntegerField(read_only=True)
    total_rs = serializers.IntegerField(read_only=True)
    cheque_no = serializers.CharField(allow_null=True)
    admission_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    ot_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    discharge_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    invoice_date = serializers.DateField(format="%d-%m-%Y")
    payment = serializers.CharField(required=True)
    class Meta:
        model = PatientBillingModel
        exclude = ('created_at', 'patient')


