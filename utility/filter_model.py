import re

from django.db.models import Q


def camel_to_snake(variable_name):
    variable_name = re.sub(r'(?<!^)(?=[A-Z])', '_', variable_name).lower()
    return variable_name


class ModelFilterUSER:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "first_name":
                model = model.filter(first_name__icontains=fld_value)
            if fld_name == "middle_name":
                model = model.filter(middle_name__icontains=fld_value)
            if fld_name == "last_name":
                model = model.filter(last_name__icontains=fld_value)
            if fld_name == "user_type":
                model = model.filter(user_type__icontains=fld_value)
            if fld_name == "hospital_name":
                model = model.filter(hospital_name__icontains=fld_value)
            if fld_name == "phone":
                model = model.filter(phone=fld_value)
            if fld_name == "state_id":
                model = model.filter(state_id=fld_value)
            if fld_name == "city_id":
                model = model.filter(city_id=fld_value)
            if fld_name == "area_id":
                model = model.filter(area_id=fld_value)
            if fld_name == "pincode":
                model = model.filter(pincode=fld_value)
            if fld_name == "email":
                model = model.filter(email__icontains=fld_value)
            if fld_name == "landline":
                model = model.filter(landline=fld_value)
            if fld_name == "fax_number":
                model = model.filter(fax_number=fld_value)
            if fld_name == "degree":
                model = model.filter(degree__icontains=fld_value)
            if fld_name == "speciality":
                model = model.filter(speciality__icontains=fld_value)
            if fld_name == "aadhar_card":
                model = model.filter(aadhar_card__icontains=fld_value)
            if fld_name == "registration_no":
                model = model.filter(registration_no=fld_value)
            if fld_name == "defaultLanguage_id":
                model = model.filter(default_language_id=fld_value)
            if fld_name == "designation":
                model = model.filter(designation__icontains=fld_value)
            if fld_name == "hospital_id":
                model = model.filter(hospital_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(user_type__icontains=search) |
                Q(hospital_name__icontains=search) |
                Q(area__icontains=search) |
                Q(phone__icontains=search) |
                Q(state__state_name__icontains=search) |
                Q(city__city_name__icontains=search) |
                Q(email__icontains=search) |
                Q(landline__icontains=search) |
                Q(fax_number__icontains=search) |
                Q(degree__icontains=search) |
                Q(speciality__icontains=search) |
                Q(aadhar_card__icontains=search) |
                Q(registration_no__icontains=search) |
                Q(default_language__language__icontains=search) |
                Q(designation__icontains=search) |
                Q(username__icontains=search) |
                Q(hospital_id__hospital_name__icontains=search)
            )
        return model


class ModelFilterCITY:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "city_name":
                model = model.filter(city_name__icontains=fld_value)
            if fld_name == "taluka_id":
                model = model.filter(taluka_id=fld_value)
            if fld_name == "city_id":
                model = model.filter(city_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(city_name__icontains=search) |
                Q(taluka__taluka_name__icontains=search) |
                Q(taluka__district__district_name__icontains=search) |
                Q(taluka__district__state__state_name__icontains=search)
            )
        return model


class ModelFilterDISTRICT:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "district_name":
                model = model.filter(district_name__icontains=fld_value)
            if fld_name == "state_id":
                model = model.filter(state_id=fld_value)
            if fld_name == "district_id":
                model = model.filter(district_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(district_name__icontains=search) |
                Q(state__state_name__icontains=search)
            )
        return model


class ModelFilterTALUKA:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "taluka_name":
                model = model.filter(taluka_name__icontains=fld_value)
            if fld_name == "district_id":
                model = model.filter(district_id=fld_value)
            if fld_name == "taluka_id":
                model = model.filter(taluka_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(taluka_name__icontains=search) |
                Q(district__district_name__icontains=search) |
                Q(district__state__state_name__icontains=search)
            )
        return model


class ModelFilterSTATE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "state_name":
                model = model.filter(state_name__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(state_name__icontains=search)
            )
        return model


class ModelFilterLANGUAGE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "language":
                model = model.filter(language__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(language__icontains=search)
            )
        return model


class ModelFilterDIAGNOSIS:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "diagnosis_name":
                model = model.filter(diagnosis_name__icontains=fld_value)
            if fld_name == "ut_weeks":
                model = model.filter(ut_weeks=fld_value)
            if fld_name == "ut_days":
                model = model.filter(ut_days=fld_value)
            if fld_name == 'diagnosis_type':
                model = model.filter(diagnosis_type__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            if search.isnumeric():
                model = model.filter(
                    Q(ut_weeks=search) |
                    Q(ut_days=search)
                )
            else:
                model = model.filter(
                    Q(diagnosis_name__icontains=search) |
                    Q(diagnosis_name__icontains=search) |
                    Q(medicine__medicine__icontains=search) |
                    Q(diagnosis_type__icontains=search)
                )
        return model


class ModelFilterMEDICINE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "medicine":
                model = model.filter(medicine__icontains=fld_value)
            if fld_name == "contain":
                model = model.filter(contain__icontains=fld_value)
            if fld_name == "medicine_type":
                model = model.filter(
                    medicine_type__medicine_type__icontains=fld_value)
            if fld_name == "per_day":
                model = model.filter(per_day=fld_value)
            if fld_name == "for_day":
                model = model.filter(for_day=fld_value)
            if fld_name == "company":
                model = model.filter(company=fld_value)
            if fld_name == "diagnosis_id":
                model = model.filter(diagnosismodel__diagnosis_id=fld_value)
            if fld_name == "ut_weeks":
                model = model.filter(diagnosismodel__ut_weeks=fld_value)
            if fld_name == "ut_days":
                model = model.filter(diagnosismodel__ut_days=fld_value)

        model = model.distinct()
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            if search.isnumeric():
                model = model.filter(
                    Q(diagnosismodel__diagnosis_id=search) |
                    Q(diagnosismodel__ut_weeks=search) |
                    Q(diagnosismodel__ut_days=search)
                )
            else:
                model = model.filter(
                    Q(medicine__icontains=search) |
                    Q(contain__icontains=search) |
                    Q(company__icontains=search) |
                    Q(morning_timing__timing__icontains=search) |
                    Q(noon_timing__timing__icontains=search) |
                    Q(evening_timing__timing__icontains=search) |
                    Q(bed_timing__timing__icontains=search) |
                    Q(medicine_type__medicine_type__icontains=search) |
                    Q(diagnosismodel__diagnosis_name__icontains=search)
                )
        return model


class ModelFilterMEDICINEOR:
    def filter_fields(self, model, filter_fields):

        filter_fields_dict = {}
        for ffields in filter_fields:
            fld_name, fld_val = ffields.split("=")
            filter_fields_dict[fld_name] = fld_val

        if "diagnosis_id" in filter_fields_dict and "ut_days" in filter_fields_dict and "ut_weeks" in filter_fields_dict:
            model = model.filter(
                Q(diagnosismodel__diagnosis_id=filter_fields_dict["diagnosis_id"]) | Q(diagnosismodel__deleted=0,
                                                                                       diagnosismodel__ut_days=filter_fields_dict[
                                                                                           "ut_days"],
                                                                                       diagnosismodel__ut_weeks=filter_fields_dict["ut_weeks"]))
        elif "diagnosis_id" not in filter_fields_dict and "ut_days" in filter_fields_dict and "ut_weeks" in filter_fields_dict:
            model = model.filter(diagnosismodel__deleted=0, diagnosismodel__ut_days=filter_fields_dict["ut_days"],
                                 diagnosismodel__ut_weeks=filter_fields_dict["ut_weeks"])
        elif "diagnosis_id" in filter_fields_dict and "ut_days" not in filter_fields_dict and "ut_weeks" not in filter_fields_dict:
            model = model.filter(
                diagnosismodel__diagnosis_id=filter_fields_dict["diagnosis_id"])

        model = model.distinct()
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            if search.isnumeric():
                model = model.filter(
                    Q(diagnosismodel__diagnosis_id=search) |
                    Q(diagnosismodel__ut_weeks=search) |
                    Q(diagnosismodel__ut_days=search)
                )
            else:
                model = model.filter(
                    Q(medicine__icontains=search) |
                    Q(contain__icontains=search) |
                    Q(company__icontains=search) |
                    Q(morning_timing__timing__icontains=search) |
                    Q(noon_timing__timing__icontains=search) |
                    Q(evening_timing__timing__icontains=search) |
                    Q(bed_timing__timing__icontains=search) |
                    Q(medicine_type__medicine_type__icontains=search) |
                    Q(diagnosismodel__diagnosis_name__icontains=search)
                )
        return model


class ModelFilterMEDICINETYPE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "medicine_type":
                model = model.filter(medicine_type__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(medicine_type__icontains=search)
            )
        return model


class ModelFilterSURGICALITEM:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "drug_name":
                model = model.filter(drug_name__icontains=fld_value)
            if fld_name == "batch_number":
                model = model.filter(batch_number__icontains=fld_value)
            if fld_name == "mfg_date":
                model = model.filter(mfg_date=fld_value)
            if fld_name == "exp_date":
                model = model.filter(exp_date=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(drug_name__icontains=search) |
                Q(batch_number__icontains=search)
            )
        return model


class ModelFilterSURGICALITEMGROUP:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "drug_group_name":
                model = model.filter(drug_group_name__icontains=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(drug_group_name__icontains=search) |
                Q(surgical_item__drug_name__icontains=search)
            )
        return model


class ModelFilterFIELDMASTER:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "field_master_name":
                model = model.filter(field_master_name__icontains=fld_value)
            if fld_name == 'field_master_id':
                model = model.filter(field_master_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(field_master_name__icontains=search)
            )
        return model


class ModelFilterMANAGEFIELDS:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "field_value":
                model = model.filter(field_value__icontains=fld_value)
            if fld_name == "field_master":
                model = model.filter(field_master_id=fld_value)
            if fld_name == 'field_master_name':
                model = model.filter(
                    field_master__field_master_name__icontains=fld_value)
            if fld_name == 'language':
                model = model.filter(language_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(field_master__field_master_name__icontains=search) |
                Q(field_value__icontains=search) |
                Q(language__language__icontains=search)
            )
        return model


class ModelFilterADVICE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "advice":
                model = model.filter(advice__icontains=fld_value)
            if fld_name == "advice_for":
                model = model.filter(advice_for=fld_value)
            if fld_name == "detail":
                model = model.filter(detail=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(advice__icontains=search) |
                Q(advice_for__icontains=search) |
                Q(detail__icontains=search)
            )
        return model


class ModelFilterADVICEGROUP:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "advice_group":
                model = model.filter(advice_group__icontains=fld_value)
            if fld_name == "advice_group_id":
                model = model.filter(advice_group__id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(advice_group__icontains=search) |
                Q(advice__advice__icontains=search)
            )
        return model


class ModelFilterTIMING:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == 'timing':
                model = model.filter(timing__icontains=fld_value)
            if fld_name == "language_name":
                model = model.filter(language__language__icontains=fld_value)
            if fld_name == "code":
                model = model.filter(language__code__icontains=fld_value)
            if fld_name == "language":
                model = model.filter(language_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(timing__icontains=search) |
                Q(language__code__icontains=search) |
                Q(language__language__icontains=search)
            )
        return model


class ModelFilterCONSULTATION:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "uid":
                model = model.filter(uid__icontains=fld_value)
            if fld_name == "parity":
                model = model.filter(parity=fld_value)
            if fld_name == "patient_type":
                model = model.filter(patient_type=fld_value)
            if fld_name == "patient_detail":
                model = model.filter(patient_detail=fld_value)
            if fld_name == "prev_del_type":
                model = model.filter(prev_del_type=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "ftnd_male_live":
                model = model.filter(ftnd_male_live=fld_value)
            if fld_name == "ftnd_male_dead":
                model = model.filter(ftnd_male_dead=fld_value)
            if fld_name == "ftnd_female_live":
                model = model.filter(ftnd_female_live=fld_value)
            if fld_name == "ftnd_female_dead":
                model = model.filter(ftnd_female_dead=fld_value)
            if fld_name == "ftlscs_male_live":
                model = model.filter(ftlscs_male_live=fld_value)
            if fld_name == "ftlscs_male_dead":
                model = model.filter(ftlscs_male_dead=fld_value)
            if fld_name == "ftlscs_female_live":
                model = model.filter(ftlscs_female_live=fld_value)
            if fld_name == "ftlscs_female_dead":
                model = model.filter(ftlscs_female_dead=fld_value)
            if fld_name == 'lmp_date':
                model = model.filter(lmp_date=fld_value)
            if fld_name == 'opd_date':
                model = model.filter(opd_date=fld_value)
            if fld_name == 'edd_date':
                model = model.filter(edd_date=fld_value)
            if fld_name == 'possible_lmp':
                model = model.filter(possible_lmp=fld_value)
            if fld_name == 'possible_edd':
                model = model.filter(possible_edd=fld_value)
            if fld_name == 'fu_date':
                model = model.filter(fu_date=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no=search) |
                Q(patient__first_name__icontains=search) |
                Q(patient__middle_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__grand_father_name__icontains=search) |
                Q(patient__registration_no__icontains=search) |
                Q(patient_type__icontains=search) |
                Q(patient_detail__icontains=search) |
                Q(parity__icontains=search) |
                Q(prev_del_type__icontains=search)
            )
        return model


class ModelFilterPATIENTPRESCRIPTION:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__iexact=search) |
                Q(diagnosis__diagnosis_name=search)
            )
        return model


class ModelFilterPATIENT:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_id":
                model = model.filter(patient_id=fld_value)
            if fld_name == "registered_no":
                model = model.filter(registered_no=fld_value)
            if fld_name == "grand_father_name":
                model = model.filter(grand_father_name__icontains=fld_value)
            if fld_name == "husband_father_name":
                model = model.filter(husband_father_name__icontains=fld_value)
            if fld_name == "taluka":
                model = model.filter(taluka__icontains=fld_value)
            if fld_name == "district":
                model = model.filter(district__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(first_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone=search) |
                Q(registered_no=search) |
                Q(grand_father_name__icontains=search) |
                Q(husband_father_name__icontains=search) |
                Q(taluka__taluka_name__icontains=search) |
                Q(district__district_name__icontains=search)
            )
        return model


class ModelFilterPATIENTOPD:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_id":
                model = model.filter(patient_id=fld_value)
            if fld_name == "opd_date":
                model = model.filter(opd_date=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "first_name":
                model = model.filter(patient__first_name__icontains=fld_value)
            if fld_name == "last_name":
                model = model.filter(patient__last_name__icontains=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(patient__first_name=search) |
                Q(patient__middle_name=search) |
                Q(patient__last_name=search) |
                Q(patient__registered_no=search) |
                Q(patient__phone__icontains=search) |
                Q(patient__patient_type__icontains=search) |
                Q(patient__patient_detail__icontains=search) |
                Q(patient__husband_father_name__icontains=search) |
                Q(patient__grand_father_name__icontains=search) |
                Q(patient__city__city_name__icontains=search) |
                Q(regd_no__iexact=search)
            )
        return model


class ModelFilterPATIENTREFERAL:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_id":
                model = model.filter(patient_id=fld_value)
            if fld_name == "patient_referal_id":
                model = model.filter(patient_referal_id=fld_value)
            if fld_name == "indication":
                model = model.filter(indication__icontains=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(patient__first_name=search) |
                Q(patient__middle_name=search) |
                Q(patient__last_name=search) |
                Q(patient__phone=search) |
                Q(indication=search)
            )
        return model


class ModelFilterPATIENTUSGFORM:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_id":
                model = model.filter(patient_id=fld_value)
            if fld_name == "patient_usgform_id":
                model = model.filter(patient_usgform_id=fld_value)
            if fld_name == "diagnosis":
                model = model.filter(
                    diagnosis__diagnosis_name__icontains=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(patient__first_name=search) |
                Q(patient__middle_name=search) |
                Q(patient__last_name=search) |
                Q(patient__phone=search) |
                Q(diagnosis__dianosis_name=search)
            )
        return model


class ModelFilterUSGFORMCHILD:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "usgform_child_id":
                model = model.filter(usgform_child_id=fld_value)
            if fld_name == "child_gender":
                model = model.filter(child_gender=fld_value)
            if fld_name == "child_year":
                model = model.filter(child_year=fld_value)
            if fld_name == "child_month":
                model = model.filter(child_month=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(child_gender=search)
            )
        return model


class ModelFilterPATIENTDISCHARGE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_discharge_id":
                model = model.filter(patient_discharge_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "admission_date":
                model = model.filter(admission_date=fld_value)
            if fld_name == "admission_time":
                model = model.filter(admission_time=fld_value)
            if fld_name == "complain_of":
                model = model.filter(complain_of__icontains=fld_value)
            if fld_name == "diagnosis":
                model = model.filter(diagnosis__diagnosis_name=fld_value)
            if fld_name == "name_of_operation":
                model = model.filter(name_of_operation__icontains=fld_value)
            if fld_name == "ot_date":
                model = model.filter(ot_date=fld_value)
            if fld_name == "ot_time":
                model = model.filter(ot_time=fld_value)
            if fld_name == "treatment_given":
                model = model.filter(treatment_given__icontains=fld_value)
            if fld_name == "advice":
                model = model.filter(advice__advice__icontains=fld_value)
            if fld_name == "any_history":
                model = model.filter(any_history__icontains=fld_value)
            if fld_name == "assisted":
                model = model.filter(assisted__icontains=fld_value)
            if fld_name == "discharge_date":
                model = model.filter(discharge_date=fld_value)
            if fld_name == "discharge_time":
                model = model.filter(discharge_time=fld_value)
            if fld_name == "remark":
                model = model.filter(remark__icontains=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(complain_of__icontains=search) |
                Q(diagnosis__diagnosis_name__icontains=search) |
                Q(name_of_operation__icontains=search) |
                Q(treatment_given__icontains=search) |
                Q(advice__advice__icontains=search) |
                Q(any_history__icontains=search) |
                Q(assisted__icontains=search) |
                Q(remark__icontains=search)
            )
        return model


class ModelFilterPATIENTUSGREPORT:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_usgreport_id":
                model = model.filter(patient_usgreport_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "report_date":
                model = model.filter(report_date=fld_value)
            if fld_name == "anomalies":
                model = model.filter(anomalies_icontains=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(anomalies__icontains=search) |
                Q(regd_no__icontains=search) |
                Q(cardiac_activity__icontains=search) |
                Q(presentation__icontains=search) |
                Q(possible_lmp__icontains=search) |
                Q(placental_location__icontains=search) |
                Q(amount_of_liquor__icontains=search) |
                Q(remark__icontains=search) |
                Q(usg_report__icontains=search)
            )
        return model


class ModelFilterPATIENTOVULATIONPROFILE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_ovulation_profile_id":
                model = model.filter(patient_ovulation_profile_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "op_day":
                model = model.filter(op_day=fld_value)
            if fld_name == "op_date":
                model = model.filter(op_date=fld_value)
            if fld_name == "ut_blood_flow":
                model = model.filter(ut_blood_flow__icontains=fld_value)
            if fld_name == "diagnosis":
                model = model.filter(ovarian_blood_flow=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(ut_blood_flow__icontains=search) |
                Q(ovarian_blood_flow__icontains=search)
            )
        return model


class ModelFilterPATIENTMTP:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_mtp_id":
                model = model.filter(patient_mtp_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "second_rmp":
                model = model.filter(second_rmp=fld_value)
            if fld_name == "op_date":
                model = model.filter(op_date=fld_value)
            if fld_name == "reason_for_mtp":
                model = model.filter(reason_for_mtp__icontains=fld_value)
            if fld_name == "contraception":
                model = model.filter(contraception__icontains=fld_value)
            if fld_name == "mtp_complication":
                model = model.filter(mtp_complication__icontains=fld_value)
            if fld_name == "discharge_date":
                model = model.filter(discharge_date=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(second_rmp__icontains=search) |
                Q(contraception__icontains=search) |
                Q(mtp_complication__icontains=search) |
                Q(remark__icontains=search)
            )
        return model


class ModelFilterPATIENTHISTOLAP:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_histolap_id":
                model = model.filter(patient_histolap_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "admission_date":
                model = model.filter(admission_date=fld_value)
            if fld_name == "procedure_name":
                model = model.filter(procedure_name=fld_value)
            if fld_name == "discharge_date":
                model = model.filter(discharge_date=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(procedure_name__icontains=search)
            )
        return model


class ModelFilterPATIENTBILLING:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_billing_id":
                model = model.filter(patient_billing_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "invoice_no":
                model = model.filter(invoice_no=fld_value)
            if fld_name == "admission_date":
                model = model.filter(admission_date=fld_value)
            if fld_name == "ot_date":
                model = model.filter(ot_date=fld_value)
            if fld_name == "discharge_date":
                model = model.filter(discharge_date=fld_value)
            if fld_name == "diagnosis":
                model = model.filter(diagnosis_id=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(invoice_no__icontains=search)
            )
        return model


class ModelFilterPATIENTVOUCHER:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_voucher_id":
                model = model.filter(patient_voucher_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "voucher_no":
                model = model.filter(voucher_no__icontains=fld_value)
            if fld_name == "bill_date":
                model = model.filter(bill_date=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(voucher_no__icontains=search)
            )
        return model


class ModelFilterVOUCHERITEM:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "surgical_item_id":
                model = model.filter(surgical_item_id=fld_value)
            if fld_name == "surgical_item":
                model = model.filter(surgical_item_id=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(surgical_item__drug_name_icontains=search)
            )
        return model


class ModelFilterPATIENTINDOOR:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_indoor_id":
                model = model.filter(patient_indoor_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "indoor_case_number":
                model = model.filter(indoor_case_number__icontains=fld_value)
            if fld_name == "indoor_date":
                model = model.filter(indoor_date=fld_value)
            if fld_name == "indoor_time":
                model = model.filter(indoor_time=fld_value)
            if fld_name == "complain":
                model = model.filter(complain__icontains=fld_value)
            if fld_name == "diagnosis":
                model = model.filter(diagnosis_id=fld_value)
            if fld_name == "operation":
                model = model.filter(operation__icontains=fld_value)
            if fld_name == "patient_opd_id":
                model = model.filter(patient_opd_id=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(indoor_case_number__icontains=search) |
                Q(complain__icontains=search) |
                Q(contraception__icontains=search) |
                Q(operation__icontains=search) |
                Q(diagnosis__diagnosis_name__icontains=search)
            )
        return model


class ModelFilterINDOORADVICE:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_mtp_id":
                model = model.filter(patient_mtp_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "second_rmp":
                model = model.filter(second_rmp=fld_value)
            if fld_name == "op_date":
                model = model.filter(op_date=fld_value)
            if fld_name == "reason_for_mtp":
                model = model.filter(reason_for_mtp__icontains=fld_value)
            if fld_name == "contraception":
                model = model.filter(contraception__icontains=fld_value)
            if fld_name == "mtp_complication":
                model = model.filter(mtp_complication__icontains=fld_value)
            if fld_name == "discharge_date":
                model = model.filter(discharge_date=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(regd_no__icontains=search) |
                Q(second_rmp_icontains=search) |
                Q(reason_for_mtp__icontains=search) |
                Q(contraception__icontains=search) |
                Q(mtp_complication__icontains=search) |
                Q(remark__icontains=search)
            )
        return model


class ModelFilterTEMPLATEHEADER:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "template_header":
                model = model.filter(template_header__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(template_header__icontains=search) |
                Q(language__language__icontains=search)
            )
        return model


class ModelFilterPATIENTDELIVERY:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_delivery_id":
                model = model.filter(patient_delivery_id=fld_value)
            if fld_name == "regd_no":
                model = model.filter(regd_no=fld_value)
            if fld_name == "baby_no":
                model = model.filter(baby_no=fld_value)
            if fld_name == "child_name":
                model = model.filter(child_name__icontains=fld_value)
            if fld_name == "birth_date":
                model = model.filter(birth_date__date=fld_value)
            if fld_name == "village":
                model = model.filter(village__icontains=fld_value)
            if fld_name == "taluka":
                model = model.filter(taluka__icontains=fld_value)
            if fld_name == "district":
                model = model.filter(district__icontains=fld_value)
            if fld_name == "first_name":
                model = model.filter(patient__first_name__icontains=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            if search.isnumeric():
                model = model.filter(
                    Q(patient_delivery_id=search) |
                    Q(regd_no=search) |
                    Q(baby_no=search)
                )
            else:
                model = model.filter(
                    Q(district__icontains=search) |
                    Q(taluka__icontains=search) |
                    Q(village__icontains=search) |
                    Q(child_name__icontains=search) |
                    Q(patient__first_name__icontains=search)
                )
        return model
