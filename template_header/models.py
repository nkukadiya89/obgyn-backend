from django.db import models
from language.models import LanguageModel
from django.utils.timezone import now

# Create your models here.
class TemplateHeaderModel(models.Model):
    template_header_id = models.AutoField(primary_key=True)
    template_header_name = models.CharField(max_length=35, default="", null=True)
    language = models.ForeignKey(LanguageModel, on_delete=models.DO_NOTHING)
    header_text = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.template_header_id})"

    class Meta:
        db_table = "template_header"
