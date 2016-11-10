""" Nota: Los macros deben estar especificados en un modulo dentro del excel. """

import read_xl
import os
import easygui

import xlwings as xl
import excel_macro as macro_xl
import list_extractor as lx
from Extractor_plantilla import Extractor_plantilla
from CFDI import CFDI_Obj
import datetime as dt
from operator import attrgetter

headings = ["SubTotal", "Descuento", "Subtotal Neto", "Base 0", "16% IVA", "No deducible", "Total", "Diferencias",
            "Notas"]
sheet_name = "Sheet1"

#####################
plantilla = Extractor_plantilla()
IVA_ref = plantilla.data_dict.get('IVA')
Total_ref = plantilla.data_dict.get('Total')
Imp_tras_ref = plantilla.data_dict.get('ImpTrasladados')
RFC_Emisor_ref = plantilla.data_dict.get('RFC Emisor')
Number_ref = plantilla.data_dict.get('Number')
subtotal_ref = plantilla.data_dict.get("Subtotal")
ivaRetenido_ref = plantilla.data_dict.get("ivaRetenido")
isrRetenido_ref = plantilla.data_dict.get("isrRetenido")
descuento_ref = plantilla.data_dict.get("Descuento")
fecha_ref = plantilla.data_dict.get("Fecha")


workbook_dir = easygui.fileopenbox()
data = read_xl.ExcelReadtoList(workbook_dir)


############################################################
# Referencias - Encabezados
index_ref = data.get(sheet_name)[0:1]

# create objects for each CFDI

Facturas_list = []
""":type: list of CFDI_Obj"""

for values in data.get(sheet_name)[1:]:
    IVA = values[lx.row_search_index_data_2dlist(IVA_ref, index_ref)]
    Total = values[lx.row_search_index_data_2dlist(Total_ref, index_ref)]
    Imp_tras = values[lx.row_search_index_data_2dlist(Imp_tras_ref, index_ref)]
    RFC_Emisor = values[lx.row_search_index_data_2dlist(RFC_Emisor_ref, index_ref)]
    Num = values[lx.row_search_index_data_2dlist(Number_ref, index_ref)]
    subtotal_cfdi = values[lx.row_search_index_data_2dlist(subtotal_ref, index_ref)]
    ivaRetenido = values[lx.row_search_index_data_2dlist(ivaRetenido_ref, index_ref)]
    isrRetenido = values[lx.row_search_index_data_2dlist(isrRetenido_ref, index_ref)]
    descuento = values[lx.row_search_index_data_2dlist(descuento_ref, index_ref)]

    time = values[lx.row_search_index_data_2dlist(fecha_ref, index_ref)]
    date_time = dt.datetime.strptime(time, "%Y-%m-%dT%X")

    d = {}

    for reference in index_ref[0]:
        # print(index_ref)
        if reference is not None:
            # print(reference)
            d[reference] = values[lx.row_search_index_data_2dlist(reference, index_ref)]

    d_update = {'IVA': IVA, 'total': Total, 'Imp_tras': Imp_tras, 'RFC_E': RFC_Emisor, 'num': Num,
                'SubTotal_cfdi': subtotal_cfdi, 'fecha': date_time,
                'ivaRetenido': ivaRetenido, 'isrRetenido': isrRetenido, 'descuento': descuento}

    d.update(d_update)

    for key, value in d.items():
        if value is not None and not str and not dt.datetime:
            print(key, value)
            d[key] = round(value, 8)

    Factura = CFDI_Obj(d)
    Factura.__dict__.update(d)

    Facturas_list.append(Factura)  # this is all data, sorted or unsorted

# Calculate all the values of interest
for item in Facturas_list:

    print("##############################################")
    if item.total < 0.00001:
        print(item.num, " ", "Es cero")
        continue

    print(item.num, ' ', item.RFC_E)
    print('Fecha: ', item.fecha.day, item.fecha.month, item.fecha.year)
    print('Iva: ', item.IVA, 'Subtotal_CFDI: ', item.SubTotal_cfdi)
    print("Total: ", item.total, 'Descuento: ', item.descuento)

    if (item.ivaRetenido or item.isrRetenido) is not None:

        if (item.ivaRetenido or item.isrRetenido) > 0.001:
            item.nota = 'Imp Retenidos '

            if item.descuento is not None:
                comparative_test = abs((item.SubTotal_cfdi - item.descuento) * 0.16 - item.IVA)
            else:
                comparative_test = abs(item.SubTotal_cfdi * 0.16 - item.IVA)

            total = item.IVA + item.SubTotal_cfdi
            ivaRetenido_test = item.SubTotal_cfdi * 0.16 / 3 * 2
            isrRetenido_test = item.SubTotal_cfdi * 0.1

            if item.isrRetenido is not None:
                validate = abs(item.isrRetenido - isrRetenido_test)
                if validate <= 0.01:
                    total = total - item.isrRetenido
                    print(total, "isr retenido")
                else:
                    total = total - item.ivaRetenido
                    print(total, "isr retenido - Differences")
                    item.nota += "checar ISR "

            if item.ivaRetenido is not None:
                print(item.ivaRetenido, ivaRetenido_test)
                validate = abs(item.ivaRetenido - ivaRetenido_test)
                if validate <= 0.01:
                    total = total - item.ivaRetenido
                    print(total, "iva retenido")
                else:
                    total = total - item.ivaRetenido
                    print(total, "iva retenido - Differences")
                    item.nota += "checar IVA "

            item.total = total
            item.nota += '- ISR o IVA Retenido '
            item.SubTotal = item.SubTotal_cfdi
            continue

    try:
        if item.descuento is not None:
            comparative_test = abs((item.SubTotal_cfdi - item.descuento) * 0.16 - item.IVA)
        else:
            comparative_test = abs(item.SubTotal_cfdi * 0.16 - item.IVA)

        if comparative_test <= 0.01:
            if abs((item.IVA + item.SubTotal_cfdi) - item.total) <= 0.01:
                item.SubTotal = item.SubTotal_cfdi
                continue
            elif item.descuento is not None and \
                            abs((item.IVA + item.SubTotal_cfdi - item.descuento) - item.total) <= 0.01:
                item.SubTotal = item.SubTotal_cfdi - item.descuento

                continue

    except:
        item.nota = 'Revisar'

    iva_buffer = 0
    if item.IVA is not None:
        iva_buffer = item.IVA

    if item.IVA is None:
        item.nota = "REVISAR IVA"
        item.SubTotal = item.SubTotal_cfdi

    else:

        item.SubTotal = item.IVA / .16
        item.buffer = item.SubTotal * .16
        print("processing else case")
        # print("sum: ", abs(object_ref.buffer + object_ref.SubTotal - object_ref.total))
        if abs(item.buffer + item.SubTotal - item.total) > 0.001:
            item.base_cero = item.total - item.buffer - item.SubTotal

            if item.base_cero < 0:
                print("     inside if 1")
                item.SubTotal = item.SubTotal_cfdi
                # object_ref.IVA = object_ref.SubTotal * .16  --- Iva is the same in cfdi
                item.base_cero = item.total - item.SubTotal - item.IVA

            if item.base_cero < 0:
                print("     inside if 2")
                if item.descuento is not None:
                    item.SubTotal = item.SubTotal_cfdi - item.descuento
                    item.IVA = iva_buffer
                    item.base_cero = 0
                    item.total = item.SubTotal + item.IVA

                    # todo: if sum of subtotal + iva > total, subtotal = subtotal  + subtotal*.16 + base0 = total

    print("Subtotal: ", item.SubTotal)
    print("Base 0: ", item.base_cero)

##############################################################################################
# Sort the values by year and split them in an array for months

split_by_year = input("Realizar por mes y año en un archivo diferente? [y/n]")
if split_by_year == 'y':


    facturas_sort = sorted(Facturas_list, key=attrgetter('fecha.year'))
    """:type: list of CFDI_Obj"""

    from collections import defaultdict


    d_year_month = defaultdict(lambda: defaultdict(list))
    """:type: defaultdict[int, dict[int, list of CFDI_Obj]"""

    for item in facturas_sort:

        d_year_month[item.fecha.year][item.fecha.month].append(item)
        print(item.num, item.fecha.year)


    counter = 1
    wb = xl.Book(workbook_dir)
    for year, values in d_year_month.items():

        year_book = xl.App(add_book=False)
        workbook = xl.Book()

        print(year)

        active_sheet = xl.sheets['Sheet1']  # type: xl.Sheet



        for month, facturas in values.items():
            print(month)
            month_names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto',
                           'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            print(month-1)
            xl.sheets.add(name=month_names[month - 1], after=active_sheet)
            active_sheet = xl.sheets[month_names[month-1]]  # type: xl.Sheet



            insert_list_CFDI = [index_ref[0]]
            insert_list = [headings]
            for cfdi in facturas:
                assert isinstance(cfdi, CFDI_Obj)

                row = []
                for index in index_ref[0]:
                    row.append(cfdi.aditional_properties.get(index))
                    print("index: ", index, "value: ", cfdi.aditional_properties.get(index))

                insert_list_CFDI.append(row)

                cfdi.SubTotal_pre_descuento = cfdi.SubTotal
                print("processing: ", cfdi.num, cfdi.descuento, cfdi.SubTotal_pre_descuento, cfdi.SubTotal)

                if cfdi.descuento is not None and cfdi.SubTotal is not None:
                    cfdi.SubTotal_pre_descuento = cfdi.descuento + cfdi.SubTotal

                insert_list.append(
                    [cfdi.SubTotal_pre_descuento, cfdi.descuento, cfdi.SubTotal, cfdi.base_cero, cfdi.IVA, 0, cfdi.total,
                     "formula", cfdi.nota])

            active_sheet.range('A1').value = insert_list_CFDI

            active_sheet.activate()
            insert_coord = macro_xl.insert_col_after("SubTotal", wb, 9, index_ref, 0, modify_index=False)

            workbook.activate()
            active_sheet.activate()
            active_sheet.range((1, insert_coord)).value = insert_list

            # quit()

        buffer_sheet = xl.sheets['Sheet1']  # type: xl.Sheet
        buffer_sheet.activate()
        buffer_sheet.delete()

        save_dir = r'D:\Desktop'
        xl.Book('Book' + str(counter)).save(save_dir + '\\' + str(year))
        counter += 1
        workbook.close()

        # year_book.kill()
        year_book.quit()
else:
    pass

#################################################################################################
question = input("Desea continuar con la base de datos? [y/n]  ")

if question == 'y':
    pass
else:
    print("finish")
    quit()

# insertar 8 columnas a la izquierda de subtotal


app = xl.App(add_book=False)
wb = xl.Book(workbook_dir)
wb.activate()
active_sheet = wb.sheets['Sheet1']  # type: Sheet
active_sheet.activate()
print(index_ref)
insert_coord = macro_xl.insert_col_after("SubTotal", wb, 9, index_ref, 0)
print(insert_coord)
# Insert Headings

insert_list = [headings]
for item in Facturas_list:
    # print(item.SubTotal)
    # ["SubTotal", "Descuento", "Subtotal Neto", "Base 0", "16% IVA", "No deducible", "Total", "Diferencias"]

    item.SubTotal_pre_descuento = item.SubTotal
    print("processing: ", item.num, item.descuento, item.SubTotal_pre_descuento, item.SubTotal)

    if item.descuento is not None and item.SubTotal is not None:
        item.SubTotal_pre_descuento = item.descuento + item.SubTotal

    insert_list.append([item.SubTotal_pre_descuento, item.descuento, item.SubTotal, item.base_cero, item.IVA, 0, item.total, "formula", item.nota])

print("################################")
print("Values to paste:")
lx.print_list(insert_list)

wb.sheets[sheet_name].range((1, insert_coord)).value = insert_list
