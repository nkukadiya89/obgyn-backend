from django.db import models
from django.utils.timezone import now

from language.models import LanguageModel


# Create your models here.
class ManageFieldsModel(models.Model):
    mfId = models.AutoField(primary_key=True)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True, db_column="languageId")
    fieldName = models.CharField(max_length=50, default="")
    fieldValue = models.CharField(max_length=150, default="")

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.mfId},{self.fieldName})"

    class Meta:
        db_table = "manage_field"
