from django.db import models
from django.utils.timezone import now

from language.models import LanguageModel


# Create your models here.
class ManageFieldsModel(models.Model):
    mf_id = models.AutoField(primary_key=True)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True)
    field_name = models.CharField(max_length=50, default="")
    field_value = models.CharField(max_length=150, default="")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.mf_id},{self.field_name})"

    class Meta:
        db_table = "manage_field"
