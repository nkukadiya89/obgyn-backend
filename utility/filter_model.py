import re
import datetime

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
                Q(area__icontains=search)|
                Q(phone__icontains=search)|
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
                Q(username__icontains=search)
            )
        return model

class ModelFilterCITY:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "city_name":
                model = model.filter(city_name__icontains=fld_value)
            if fld_name == "state_id":
                model = model.filter(state_id=fld_value)
            if fld_name == "city_id":
                model = model.filter(city_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(city_name__icontains=search) |
                Q(state__state_name__icontains=search)
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
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(diagnosis_name__icontains=search) |
                Q(medicine__medicine__icontains=search)
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
                model = model.filter(contain__iexat=fld_value)
            if fld_name == "medicine_type":
                model = model.filter(medicine_type__medicine_type__icontains=fld_value)
            if fld_name == "per_day":
                model = model.filter(per_day=fld_value)
            if fld_name == "for_day":
                model = model.filter(for_day=fld_value)
            if fld_name == "company":
                model = model.filter(company=fld_value)

        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(medicine__icontains=search) |
                Q(contain__icontains=search) |
                Q(company__icontains=search) |
                Q(morning_timing__timing__icontains=search) |
                Q(noon_timing__timing__icontains=search) |
                Q(evening_timing__timing__icontains=search) |
                Q(bed_timing__timing__icontains=search) |
                Q(medicine_type__medicine_type__icontains=search)
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
            if fld_name == "field_master_id":
                model = model.filter(field_master_id=fld_value)
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
            if fld_name == "language":
                model = model.filter(language__language__icontains=fld_value)
            if fld_name == "code":
                model = model.filter(language__code__icontains=fld_value)
            if fld_name == "language_id":
                model = model.filter(language=fld_value)
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
                Q(patient__first_name__icontains=search) |
                Q(patient__middle_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__grand_father_name__icontains=search) |
                Q(patient__registration_no__icontains=search) |
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
                Q(diagnosis__diagnosis_name=search) |
                Q(medicine__medicine__icontains=search)
            )
        return model

class ModelFilterPATIENT:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "patient_id":
                model = model.filter(patient_id=fld_value)
            if fld_name == "department":
                model = model.filter(department=fld_value)
            if fld_name == "patient_type":
                model = model.filter(patient_type=fld_value)
            if fld_name == "patient_detail":
                model = model.filter(patient_detail=fld_value)
            if fld_name == "registered_no":
                model = model.filter(registered_no=fld_value)
            if fld_name == "grand_father_name":
                model = model.filter(grand_father_name__icontains=fld_value)
            if fld_name == "taluka":
                model = model.filter(taluka__icontains=fld_value)
            if fld_name == "district":
                model = model.filter(district__icontains=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__middle_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__phone=search) |
                Q(department__icontains=search) |
                Q(patient_type__icontains=search) |
                Q(patient_detail__icontains=search) |
                Q(registered_no=search) |
                Q(grand_father_name__icontains=search) |
                Q(taluka__icontains=search) |
                Q(district__icontains=search)
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
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(patient__first_name=search) |
                Q(patient__middle_name=search) |
                Q(patient__last_name=search) |
                Q(patient__phone=search)
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
