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
from pricing.views_.tarificador_libraries.register import create_register, update_register, get_categories, get_register_all, update_favorite, change_state, get_count_registers


def index(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
    # Consultar categorías
    count_registers = get_count_registers()
    categories = get_categories()
    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'categories': categories.to_records(),
        'count_registers': count_registers.to_records(),
        'title': 'Administrador',
        'area': 'Pricing',
        'herramienta': 'adminTarificador',
        'file': 'pricing/tarificador_administrador.html',
    }
    return render(request, "principal/base.html", configurationView)


def table(request, category):
    log = get_register_all(category)
    data = []
    if len(log) >0:
        log['DATETIME'] = log['DATETIME'].dt.strftime('%Y-%b-%d <sup style="color: #2196F3;text-shadow: 1px 1px 5px #7372da9e;">%I:%M %p</sup>')
    for i, row in log.iterrows():
        data.append({
            "ID": str(row['ID']),
            "USER_ID": str(row['USER_ID']),
            "FIRST_NAME": str(row['FIRST_NAME']),
            "LAST_NAME": str(row['LAST_NAME']),
            "DATETIME": str(row['DATETIME']),
            "FILE_INPUT": str(row['FILE_INPUT']),
            "FILE_OUTPUT_TAN": str(row['FILE_OUTPUT_TAN']),
            "SUCCESS_TAN": str(row['SUCCESS_TAN']),
            "TOTAL_TIME_TAN": str(row['TOTAL_TIME_TAN']),
            "ERROR_TAN": str(row['ERROR_TAN']),
            "FILE_OUTPUT_BP": str(row['FILE_OUTPUT_BP']),
            "SUCCESS_BP": str(row['SUCCESS_BP']),
            "TOTAL_TIME_BP": str(row['TOTAL_TIME_BP']),
            "ERROR_BP": str(row['ERROR_BP']),
            "STATUS": str(row['STATUS']),
            "TAG": str(row['TAG']),
            "NOMBRE": str(row['NOMBRE']),
            "COLOR": str(row['COLOR'])
        })
    # Consultar categorías
    categories = get_categories()
    data2 = []
    for i, row in categories.iterrows():
        data2.append({
            "ID": str(row['ID']),
            "NOMBRE": str(row['NOMBRE']),
            "COLOR": str(row['COLOR'])
        })
    return JsonResponse({'DTable': data, 'categories': data2}, safe=False)


def change_tag(request):
    update = update_favorite(request.POST.get('id'), request.POST.get('idcategory'))
    return JsonResponse(update, safe=False)

def update_state(request):
    update = change_state(request.POST.get('id'), 0)
    return JsonResponse(update, safe=False)
