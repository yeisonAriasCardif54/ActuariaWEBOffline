from django.shortcuts import render
import platform
import os
import re

def inicio(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name


    sistema = platform.system()
    Ttotal = '20G'
    porcenUsado = 54
    MegasUsado = '54M'
    if sistema == "Linux":
        f1 = os.popen('df -h /Data --output=size')
        Ttotal = f1.read()
        Ttotal = Ttotal.split('\n')[1]

        f2= os.popen('df -h /Data --output=pcent')
        porcenUsado = f2.read()
        porcenUsado = porcenUsado.split('\n')
        porcenUsado = re.findall('\d+', porcenUsado[1])[0]

        f3 = os.popen('df -h /Data --output=used')
        MegasUsado = f3.read()
        MegasUsado = MegasUsado.split('\n')[1]

    porcenLibre = 100-int(porcenUsado)

    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'sistema': sistema,
        'Ttotal': Ttotal,
        'porcenUsado': porcenUsado,
        'MegasUsado': MegasUsado,
        'porcenLibre': porcenLibre,
        'title': 'Home Actuaría Web',
        'area': 'Home',
        'herramienta': 'Home',
        'file': 'desk/inicio.html',
    }
    return render(request, "principal/base.html", configurationView)
