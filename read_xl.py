"""
Created on Tue Dec 15 20:30:51 2015

@author: awang
@Mod: Aristh
"""

import xlwings as xw


def ExcelReadtoList(workbook_path='', row_size=2000, col_size=150, sheet=1, visible=True):
    """This Reads all values in the Workbook and Saves them in a Dict"""
    app = xw.App(visible=visible, add_book=False)
    wb = app.books.open(workbook_path)

    #wb.app.visible(True)

    #xw.App(visible=visible)

    #xw.Application(wb).visible = visible

    # Iterate over Sheets with Dictionary
    Results = {}
    # Final Result
    Result = {}

    # Row, Col and Sheet Initial Values
    endRow = row_size
    endCol = col_size
    sheetNo = sheet

    while True:
        # Iterate over all the Rows and Cols to obtain the fartest elemets in x and y
        try:
            carrier = wb.sheets(sheetNo).name

        except:

            wb.close()
            app.quit()

            print('Completed! Be noted maximum of %d rows and %d columns have been tested!!!' % (endRow, endCol))

            #xw.App(visible=True)
            #xw.Application(wb).visible = True

            return Result  # Return Dictionary

        print("Read: ", carrier)

        # quit()
        working_sheet = xw.sheets(sheetNo)   # type: xw.Sheet

        values = working_sheet.range((1, 1), (endRow, endCol)).value
        # print(values)

        Results[carrier] = values


        maxCol = 1
        for i in range(0, endRow):
            countCol = endCol - 1
            for j in range(endCol - 1, -1, -1):
                if Results[carrier][i][j] != None:
                    break
                else:
                    countCol -= 1
            if maxCol < countCol:
                maxCol = countCol


        maxRow = 1
        for i in range(0, endCol):
            countRow = endRow - 1
            for j in range(endRow - 1, -1, -1):
                if Results[carrier][j][i] != None:
                    break
                else:
                    countRow -= 1
            if maxRow < countRow:
                maxRow = countRow

        Result[carrier] = working_sheet.range((1, 1), (maxRow + 1, maxCol + 1)).value

        sheetNo += 1
        # quit()


if __name__ == '__main__':

    import tkinter as tk
    from tkinter import filedialog

    try:
        root = tk.Tk()
        root.withdraw()
        F = filedialog.askopenfilename()

        # wb = xw.Workbook(F)
        path = F

    except:
        import easygui

        # wb = xw.Workbook(easygui.fileopenbox)

        path = easygui.fileopenbox

    data = ExcelReadtoList(path)

    print(type(data))
    print(data.items())
    # Print all values in Sheets
    for keys, values in data.items():
        print(keys)
        for row in values:
            print(row)
