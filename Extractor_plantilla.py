from xlwings import Book, Sheet
import os
import easygui

class Extractor_plantilla(object):

    def __init__(self, file_name='Plantilla_Declaraciones'):

        try:
            # If this is a standalone program the defaul dir is in Temp Folder
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name + '.xlsx'))
            #print(path)
            wb = Book(path)
        except:
            print("seleccione el archivo Plantilla.xlsx")
            path = easygui.fileopenbox(None, 'Seleccione el archivo de Plantilla')
            if path == '.':
                quit()
            wb = Book(path)

        self.current_dir = os.path.split(path)[0]
        #print(self.current_dir)
        #quit()
        working_sheet = Sheet('breakdown')

        self.data_dict = working_sheet.range('A2:B100').options(dict).value
        """:type : dict"""

        print("Data values from Plantilla_Breakdown:")
        for key, values in self.data_dict.items():
            print(key, ": ", values)
        print("#####################################")

        wb.app.quit()

if __name__ == '__main__':
    plantilla = Extractor_plantilla()
    print("values")
    print(plantilla.data_dict.get('Total'))


