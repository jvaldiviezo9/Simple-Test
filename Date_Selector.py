import read_xl
import os
import easygui

import xlwings as xl
import excel_macro as macro_xl
import list_extractor as lx
from Extractor_plantilla import Extractor_plantilla
from CFDI import CFDI_Obj

import datetime as dt

sheet_name = "Sheet1"

workbook_dir = easygui.fileopenbox()
data = read_xl.ExcelReadtoList(workbook_dir)

date_ref = 'Fecha'
Number_ref = 'No.'

############################################################
# Referencias - Encabezados
index_ref = data.get(sheet_name)[0:1]

print(index_ref)
quit()
# create objects for each CFDI

Facturas_list = []
""":type: list of CFDI_Obj"""

for values in data.get(sheet_name)[1:]:
    time = values[lx.row_search_index_data_2dlist(date_ref, index_ref)]
    Num = values[lx.row_search_index_data_2dlist(Number_ref, index_ref)]

    #time = time.split('T')

    #  https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    date_time = dt.datetime.strptime(time, "%Y-%m-%dT%X")

    d = {'num': Num, 'fecha': date_time}

    Factura = CFDI_Obj()
    Factura.__dict__.update(d)

    Facturas_list.append(Factura)

for factura in Facturas_list:

    print(factura.num, "Fecha: ", factura.fecha)
    print(factura.fecha.day, factura.fecha.month, factura.fecha.year)