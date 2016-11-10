""" Seleccionar una serie de filas """
# Range("B9,3:3,8:8,13:13,15:15").Select

from xlwings import Book, books
from easygui import fileopenbox
import list_extractor as lx


def simple_test(data="test", wb=''):
    """Send a string
    :type wb: Book
    """

    macro = wb.macro("simple_test")
    macro(data)

    # wb.xl_workbook.Application.Run("simple_test", data)


def test(data=['cat', 'dog', 'snake', 'bird'], wb=''):
    """:type wb: Book"""
    animals = data
    animal_list = ""
    for animal in animals:
        animal_list += animal + "|"

    macro = wb.macro("create_validation")
    macro(animal_list)

    # wb.xl_workbook.Application.Run("create_validation", animal_list)


def column_remove_number(data='', wb=''):
    """Data of the form: "1,2,3,4
    :type wb: Book
    """

    macro = wb.macro("col_remove_number")
    macro(data)

    # wb.xl_workbook.Application.Run("col_remove_number", data)


def col_insert_number(data='', wb='', size=0):
    """Data of the form: "1,2,3,4"
    :type wb:Book
    """
    if size > 0:
        buffer = int(data)
        buffer_list = [data]
        for i in range(size - 1):
            buffer += 1
            buffer_list.append(str(buffer))

        data = ''
        for value in buffer_list:
            data += value + ','

        data = data.rstrip(',')
        # print(data)
        # print(buffer_list)

    macro = wb.macro("col_insert_number")
    macro(data)

    #wb.xl_workbook.Application.Run("col_insert_number", data)


def row_remove_number(data='', wb=""):
    """Data of the form: "1,2,3,4
    :type wb: Book
    """

    macro = wb.macro("row_remove_number")
    macro(data)

    # wb.xl_workbook.Application.Run("row_remove_number", data)


def row_insert_number(data='', wb=''):
    """Data of the form: "1,2,3,4
    :type wb: Book
    """

    macro = wb.macro("row_insert_number")
    macro(data)

    # wb.xl_workbook.Application.Run("row_insert_number", data)


def col_remove_name(data="", wb=''):
    """Data of the form: "A:A,C:C
    :type wb: Book
    """

    macro = wb.macro("col_remove_name")
    macro(data)

    # wb.xl_workbook.Application.Run("col_remove_name", data)


def insert_col_after(refword='', wb='', size=0, refdata=list(), offset=1, modify_index=True):
    """Data of the form: "A:A,C:C - By default this modify the index
    :param offset: 1 = at the right of refword, 0 = at the left of refword
    :param refdata: List of lists
    :param modify_index: Change the refdata inserting the same elements in excel for columns.
    :type wb: Workbook
    :return : int value of the searched coord
    """
    col_number = lx.row_search_index_data_2dlist(refword, refdata)
    col_number = col_number + 1 + offset
    col_insert_number(str(col_number), wb, size)

    return_value = col_number

    if modify_index is True:
        col_number = col_number - 1 - offset
        for row in refdata:
            for value in range(size):
                row.insert(col_number, "")


    return return_value
    # print("New:", refdata)


if __name__ == '__main__':
    path_file = fileopenbox()
    wb = Book(path_file)
    from read_xl import ExcelReadtoList

    references = ExcelReadtoList(path_file, close=False)

    print(references.get("Sheet1"))
    ref_data = references.get("Sheet1")

    print(ref_data)

    insert_col_after("SubTotal", wb, 4, ref_data, 0, True)
    print(ref_data)



    # col_remove_name("A:A", wb)
    # col_insert_number('1', wb, 4)
