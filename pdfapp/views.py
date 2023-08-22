from django.shortcuts import render
from . models import Item
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

# Create your views here.

def index(request):
    items=Item.objects.all()
    context={
        "items": items
    }
    return render(request, 'index.html', context)


def generate_pdf_file(request,id):
    try:
        item=Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponse("505 Not Found")
    
    data={
        'item_name':item.name,
        'item_qty':item.quantity,
    }

    pdf=render_to_pdf("pdf.html", data)
    return HttpResponse(pdf,content_type='application/pdf')

    #force download pdf file code
    if pdf:
        response=HttpResponse(pdf,content_type='application/pdf')
        filename="Item_%s.pdf" %(data['item_name'])
        content="inline; filename='%s'" %(filename)
        content="attachment; filename=%s" %(filename)
        response['Content-Disposition']=content
        return response
    return HttpResponse("Not found")



def render_to_pdf(template_src,context_dict:dict):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)

    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None
