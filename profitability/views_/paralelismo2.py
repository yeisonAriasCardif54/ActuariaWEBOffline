from obtener_presupuesto.get_data import get_data


folder = 'static/profitability/update_presupuesto'
file = folder + '/Update_Oficial_2019_VPrueba sin NA_zgxZ7YL.xlsx'


total_time, file_output = get_data(file)
print(total_time)
print(file_output)