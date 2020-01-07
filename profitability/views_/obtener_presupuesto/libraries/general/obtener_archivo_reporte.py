# Generar el archivo con el formato requerido para el reporte

import pandas as pd


# from pyexcelerate import Workbook

def obtener_archivo_reporte(archivo_reporte, OutPut):
    # writer = pd.ExcelWriter(archivo_reporte, engine='xlsxwriter')

    OutPut.to_excel(archivo_reporte, sheet_name='OutPut', index=None, float_format='%.5f', startrow=0, header=True)

    '''
    values = [OutPut.columns] + list(OutPut.values)
    wb = Workbook()
    wb.new_sheet('OutPut', data=values)
    wb.save(archivo_reporte)
    '''

    '''
    workbook  = writer.book
    worksheet = writer.sheets['OutPut']
    
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    
    format2 = workbook.add_format()
    format2.set_align('center')
    format2.set_font_size(10)
    worksheet.set_column('A:AX', 15, format2)
    
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_($ * #.##0_);_($ * (#.##0);_($ * "-"??_);_(@_)')
    worksheet.set_column('M:AL', 15, format3)
    worksheet.set_column('AV:AX', 15, format3)
    '''
    return 1
