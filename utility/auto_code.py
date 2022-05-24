from attr import field
from manage_fields.models import FieldMasterModel


def generate_slug():
    field_master = FieldMasterModel.objects.filter(deleted=0)

    for master in field_master:
        master.save()

