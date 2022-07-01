from rest_framework import serializers
from consultation.models import ConsultationModel

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from manage_fields.models import ManageFieldsModel
from patient_indoor.models import PatientIndoorModel
from .models import PatientUSGFormModel, USGFormChildModel
from user.serializers import UserSerializers
from patient_referal.models import PatientReferalModel, PatientReferalIndication
from datetime import datetime, date
from dateutil.relativedelta import *


class USGFormChildSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(USGFormChildSerializers, self).to_representation(instance)

        if "child_dob" in ret:
            ret["child_year"] = (
                date.today().year - datetime.strptime(ret["child_dob"], "%Y-%m-%d").year
            )
            ret["child_month"] = (
                date.today().month
                - datetime.strptime(ret["child_dob"], "%Y-%m-%d").month
            )

            child_dob = datetime.strptime(ret["child_dob"], "%Y-%m-%d")
            no_of_month = ((date.today().year - child_dob.year) * 12) + (
                date.today().month - child_dob.month
            )
            ret["child_year"] = int(no_of_month / 12)
            ret["child_month"] = no_of_month % 12
        return ret

    def validate(self, data):

        data["child_dob"] = (
            date.today()
            + relativedelta(years=-data["child_year"])
            + relativedelta(months=-data["child_month"])
        )
        return data

    usgform_child_id = serializers.IntegerField(read_only=True)
    child_dob = serializers.DateField(read_only=True)
    child_year = serializers.IntegerField(required=False)
    child_month = serializers.IntegerField(required=False)

    class Meta:
        model = USGFormChildModel
        exclude = ("created_at",)


class PatientUSGFormSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientUSGFormSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        if "indication" in ret:
            indication_list = {}
            for each_indication in ret["indication"]:
                indication = ManageFieldsModel.objects.get(mf_id=each_indication)
                indication_list[indication.mf_id] = indication.field_value

            ret["indication_name"] = indication_list

        if "name_of_doctor" in ret:
            ret["name_of_doctor_name"] = (
                UserSerializers(instance.name_of_doctor).data["first_name"].title()
                + " "
                + UserSerializers(instance.name_of_doctor).data["last_name"].title()
            )

        for fld_nm in ["result_of_sonography", "any_indication_mtp", "any_other"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data[
                    "field_value"
                ]

        usgform_id_list = list(PatientIndoorModel.objects.filter(patient_opd=instance.patient_opd,deleted=0).values_list('patient_indoor_id',flat=True))
        usg_child_list = USGFormChildModel.objects.filter(
            patient_usgform_id__in=usgform_id_list, deleted=0
        )
        usg_child_lst = []
        for usg_child in usg_child_list:
            usg_childs = {}
            usg_childs["usgform_child_id"] = usg_child.usgform_child_id
            usg_childs["child_gender"] = usg_child.child_gender
            no_of_month = ((date.today().year - usg_child.child_dob.year) * 12) + (
                date.today().month - usg_child.child_dob.month
            )
            usg_childs["child_year"] = int(no_of_month / 12)
            usg_childs["child_month"] = no_of_month % 12

            usg_child_lst.append(usg_childs)

        ret["usg_child"] = usg_child_lst

        consultation = ConsultationModel.objects.filter(
            patient_opd=instance.patient_opd, deleted=0
        ).first()

        if consultation:
            ret["lmp_date"] = consultation.lmp_date.strftime("%d-%m-%Y")
            ret["diagnosis_id"] = consultation.diagnosis.diagnosis_id
            ret["diagnosis_name"] = consultation.diagnosis.diagnosis_name
            ret["ut_weeks"] = consultation.ut_weeks

        patient_referal = PatientReferalModel.objects.filter(
            patient_opd=instance.patient_opd
        ).first()

        
        if patient_referal:
            referal_manage = list(
                PatientReferalIndication.objects.filter(
                    patientreferalmodel_id=patient_referal.patient_referal_id
                ).values_list("managefieldsmodel_id", flat=True)
            )
            ret["indication_id"] = referal_manage
            if len(referal_manage) > 0:
                mflist = ManageFieldsModel.objects.filter(
                    mf_id__in=referal_manage
                )
                mf_list =[]
                for mf in mflist:
                    mf_dict = {}
                    mf_dict["indication_id"] = mf.mf_id
                    mf_dict["indication_name"] = mf.field_value
                    mf_list.append(mf_dict)
                ret["indication"] = mf_list
        return ret

    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    patient_usgform_id = serializers.IntegerField(read_only=True)
    lmp_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    consent_obtained_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    procedure_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    sonography_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)

    class Meta:
        model = PatientUSGFormModel
        exclude = ("created_at", "patient")
