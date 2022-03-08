from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Camara

def index(request):
    latest_question_list = Camara.objects.order_by('-fecha_publicacion_camara')[:5]
    template = loader.get_template('ecommerce/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def oferta(request):
    latest_question_list = Camara.objects.order_by('-fecha_publicacion_camara')[:5]
    template = loader.get_template('ecommerce/oferta.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))