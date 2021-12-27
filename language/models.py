from django.db import models
from django.utils.timezone import now


# Create your models here.
class LanguageModel(models.Model):
    languageId = models.AutoField(primary_key=True)
    language = models.CharField(max_length=50)
    code = models.CharField(max_length=5, default="")

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.languageId},{self.language})"

    class Meta:
        db_table = "language"
