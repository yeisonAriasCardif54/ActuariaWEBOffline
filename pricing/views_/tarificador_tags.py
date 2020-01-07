from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import traceback
import numpy as np
import docx
from docx.shared import Pt
import xlrd
import os
import time
from django.core.files.storage import FileSystemStorage
from pricing.views_.tarificador_libraries.register import create_register, update_register, get_categories, get_register_all, update_favorite, change_state, get_count_registers, create_register_tag, get_tag_byId, update_register_tag
from django.shortcuts import redirect


def add(request):
    return render(request, "pricing/tarificador_tags.html", {})


def edit(request, tag):
    print('\n\n\n - tagtagtagtagtagtagtag - \n\n\n')
    print(tag)
    register = get_tag_byId(tag)
    return render(request, "pricing/tarificador_tags_edit.html", {'register':register.to_records()})


def save(request):
    nombre = request.POST.get('nombre')
    color = request.POST.get('color')
    registro, insert_id = create_register_tag(nombre, color)
    return redirect('/tarificador/administrador')


def update(request, tag):
    nombre = request.POST.get('nombre')
    color = request.POST.get('color')
    registro = update_register_tag(nombre, color, tag)
    return redirect('/tarificador/administrador')
