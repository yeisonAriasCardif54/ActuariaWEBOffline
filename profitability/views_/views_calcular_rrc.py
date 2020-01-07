import configparser
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from profitability.views_.calcular_rrc.get_data import get_data
import datetime
import traceback
#from user_agents import parse


def index(request):
    agent = request.META['HTTP_USER_AGENT']
    ua_string = agent
    #user_agent = parse(ua_string)
    #print(user_agent.browser.family)
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    now = datetime.datetime.now()
    years = range(now.year -1, now.year + 5)
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
    configurationView = {
        'years': years,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': 'Herramienta para generar DesembolsosSt y RRC',
        'area': 'Profitability',
        'herramienta': 'Calcular_RRC',
        'file': 'profitability/calcular_rrc.html',
    }
    return render(request, "principal/base.html", configurationView)


def generate(request):
    folder = 'static/profitability/updaterrc'

    mes = request.POST.get('mes')
    # mes = str(mes).zfill(2)
    anio = request.POST.get('anio')
    meses = request.POST.get('meses')

    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        filename = myfile.name
        file_ext = filename[-4:]
        if file_ext == 'xlsx':
            fs = FileSystemStorage(location=folder)
            filename = fs.save(myfile.name, myfile)
            file_url = fs.url(filename)
            file = folder + '/' + filename
            try:
                obtener_data, path2 = get_data(file, mes, anio, meses)
                status = 1
                message = obtener_data
                file_return = 'static/profitability/updaterrc/' + path2
            except ValueError as exp:
                obtener_data = ''
                status = 0
                message = str(exp)
                file_return = ''
            except:
                obtener_data = ''
                status = 0
                message = 'Se presento un error al momento de generar el archivo, por favor contacte con el administrador. ***' + traceback.format_exc() + ' *** '
                file_return = ''
        else:
            status = 0
            message = 'ERROR: Por favor seleccione el archivo en formato Excel (.xlsx)'
            file_return = ''
    else:
        status = 0
        message = 'ERROR: Por favor seleccione un archivo.'
        file_return = ''

    data = {"status": status, "message": message, "file_return": file_return}
    return JsonResponse(data, safe=False)
