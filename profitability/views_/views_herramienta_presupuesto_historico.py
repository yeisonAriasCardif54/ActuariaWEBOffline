from django.shortcuts import render
from django.http import JsonResponse
from profitability.views_.obtener_presupuesto.register import get_register_all


def view_history(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': 'Histórico de Herramienta de presupuesto',
        'area': 'Profitability',
        'herramienta': 'Presupuesto_historico',
        'file': 'profitability/presupuesto_historico.html',
    }
    return render(request, "principal/base.html", configurationView)


def get_history_all(request):
    log = get_register_all()
    data2 = []
    for i, row in log.iterrows():
        data2.append({
            "ID": str(row['ID']),
            "USER_ID": str(row['USER_ID']),
            "FIRST_NAME": str(row['FIRST_NAME']),
            "LAST_NAME": str(row['LAST_NAME']),
            "DATETIME": str(row['DATETIME']),
            "FILE_INPUT": str(row['FILE_INPUT']),
            "FILE_OUTPUT": str(row['FILE_OUTPUT']),
            "SUCCESS": str(row['SUCCESS']),
            "TOTAL_TIME": str(row['TOTAL_TIME']),
            "ERROR": str(row['ERROR']),
            "STATUS": str(row['STATUS']),
            "FAVORITE": str(row['FAVORITE'])
        })
    return JsonResponse(data2, safe=False)
