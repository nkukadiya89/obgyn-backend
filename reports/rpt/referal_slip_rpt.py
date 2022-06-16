from django.shortcuts import render
from template_header.models import TemplateHeaderModel

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def referal_slip_rpt(request, id, language_id=None):
    if language_id:
        template_header = TemplateHeaderModel.objects.filter(pk=1, language_id=language_id, deleted=0).first()
    else:
        template_header = TemplateHeaderModel.objects.filter(pk=1,deleted=0).first()

    if not template_header:
        raise "Template not found"

    context = {}

    template_name = "reports/en/referal_slip.html"
    return render(request, template_name,
                  {"context": context, "template_header": template_header.header_text.replace("'", "\"")})
