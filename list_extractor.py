import numpy as np
"""This is a search module that can works with the data obtained by read_xl.py"""

def list_search_index_data(refword=str, datalist=list()):
    """Base Case: search for a value in a list"""

    try:
        # print("datalist: ", datalist)
        # print(type(datalist))
        # print("refword: ", refword)
        # print(type(refword))
        value = datalist.index(refword)
        # print(value)
        return value
    except ValueError:
        print("WARNING: No search value in row of the given list: ", refword)


def col_search_index_data_2dlist(refword=str, datalist=list(), start_row=0, start_col=0):
    """Search for value in col values in a list of lists given the starting col and row"""
    index = start_row
    for index_value in datalist[start_row:]:
        if index_value[start_col] == refword:
            return index
        else:
            index += 1

    return None


def row_search_index_data_2dlist(refword=str, datalist=list(), start_row=0):
    """Search for value in row values in a list of lists given the starting row"""
    index = 0
    for index_value in datalist[start_row]:
        if index_value == refword:
            return index
        else:
            index += 1

    return None


def getCol_size(column=list(), none_tolerance=100, refword=None):
    """Gets the column size taking none tolerance or other ref word"""
    tolerance = 0
    size = 0
    for value in column:
        if value is refword:
            tolerance += 1
            if tolerance >= none_tolerance:
                break
        else:
            size += 1
    return size


def coord_search_full_list_row(refword='', datalist=list(), init_row=0, init_col=0, index1=False):
    """Search full list using rows as starting search, returns (x,y)"""
    x = None
    y = None
    counter = init_row
    for values in datalist[init_row:]:
        # print("values coord search: ", values)
        # print(refword)
        y = list_search_index_data(refword, values[init_col:]) + init_col

        if y is not None:
            x = counter

            # if index 1 is desired
            if index1 is True:
                y += 1
                x += 1
            return x, y

        counter += 1

    return x, y


def coord_search_full_list_col(refword='', datalist=list(), init_row=0, init_col=0, index1=False):
    """Search full list using columns as starting search"""
    x = None
    y = None
    for counter in range(init_col, len(datalist[0])):

        x = col_search_index_data_2dlist(refword, datalist, init_row, counter)

        if x is not None:
            y = counter

            # if index 1 is desired
            if index1 is True:
                y += 1
                x += 1
            return x, y
        counter += 1

    return x, y


def coord_search_xiyi_xfyf(xiyi='', xiyf='', xfyi='', datalist=list(), init_row=0, init_col=0, index1=False):
    """returns square section given by three points of reference"""
    start = coord_search_full_list_col(xiyi, datalist, init_row, init_col)
    finish = (col_search_index_data_2dlist(xfyi, datalist, start[0] + 1, start[1]),
              row_search_index_data_2dlist(xiyf, datalist, start[0]))

    if index1 is True:
        return (start[0] + 1, start[1] + 1), (finish[0] + 1, finish[1] + 1)

    return start, finish


def coord_search_row(xi='', xf='', datalist=list(), init_row=0, init_col=0, index1=False):
    """Search only in one row given xi and xf as references, returns ( (xi, yi), (xf, yi) )"""
    start = coord_search_full_list_row(xi, datalist, init_row, init_col)
    # print("coord_search_row: ", start)
    finish = row_search_index_data_2dlist(xf, datalist, start[0])

    if index1 is True:
        return (start[0] + 1, start[1] + 1), (start[0] + 1, finish + 1)

    return start, (start[0], finish)


def offset_coords(coords=tuple(), vertical=0, horizontal=0):
    """Simple offset of coords, down is positive, up negative, left negative, right positive"""
    return coords[0] + vertical, coords[1] + horizontal


def extract_section(init_coords=(0, 0), end_coords=(0, 0), datalist=list(), offset=1):
    """Extract a section given init coords and end coords of a datalist, index 0 given by offset. Data can be an numpy array"""
    if isinstance(datalist, type(list())):
        array = np.array(datalist)
        #todo:aslkdjflka
        print_list(array)
        array_section = array[init_coords[0]:end_coords[0] + offset, init_coords[1]:end_coords[1] + offset]
        return array_section.tolist()

    elif isinstance(datalist, type(np.array())):
        array_section = datalist[init_coords[0]:end_coords[0] + offset, init_coords[1]:end_coords[1] + offset]
        return array_section.tolist()

    return TypeError


def extract_section_col_references(xi='', xf='', datalist=list(), vertical_offset=0, heading=False,
                                   init_row=0, init_col=0, xi_horizontal_offset=0, xf_horizontal_offset=0):
    """
    Return a section of a list of lists transformed as list of lists, with vertical offset (height)
    Returns a column values given two references
    """

    if xf is None:
        return extract_col_reference(xi, datalist, vertical_offset, heading,
                                   init_row, init_col)

    row = 1
    if heading is True:
        row = 0
    working_coords = coord_search_row(xi, xf, datalist, init_row, init_col, False)
    # print(working_coords)
    return extract_section(offset_coords(working_coords[0], row, xi_horizontal_offset),
                           offset_coords(working_coords[1], vertical_offset, xf_horizontal_offset),
                           datalist)


def extract_col_reference(refword='', datalist=list(), vertical_offset=0, heading=False, init_row=0, init_col=0):
    """Return a column values from a datalist given the vertical offset and the refword. init_row and init_col
    are used to the search of references."""
    row = 1
    if heading is True:
        row = 0
    working_coords = coord_search_full_list_row(refword, datalist, init_row, init_col, False)
    return extract_section(offset_coords(working_coords, row), offset_coords(working_coords, vertical_offset), datalist)


def split_section_col_references(ref='', datalist=list(), full_list=True, vertical_offset=0, init_row=0, init_col=0,
                                 first_half_offset=0, second_half_offset=1, give_coords=False):
    """Datalist: lists of lists of same size, ref is included in the first split, modify with second_half_offset
    second_half_offset=0 included ref in the second split, first_half_offset=-1 return empty if ref is init value
    use (-1, 0) if empty list if ref is the first element is desired
    :param give_coords: if this value is True ref should be a coord tuple
    """

    if full_list is True:
        vertical_offset = len(datalist)

    horizontal = len(datalist[0])

    # Coord search using reference
    if give_coords is True:
        working_coord = ref
    else:
        working_coord = coord_search_full_list_row(ref, datalist, init_row, init_col, False)

    first_half = extract_section((0, 0), offset_coords(working_coord, vertical_offset, first_half_offset), datalist, 1)

    # print(first_half)
    second_half = extract_section(offset_coords(working_coord, 0, second_half_offset),
                                  offset_coords(working_coord, vertical_offset,
                                                               horizontal), datalist, 1)
    # print('############')
    # print(second_half)

    return first_half, second_half


def split_section_row_reference(row=0, datalist=list()):
    """Datalist: lists of lists of same size, split horizontal, row=index is included in first split"""

    width = len(datalist[0])
    height = len(datalist)

    first_half = extract_section((0, 0), (row, width), datalist, 1)

    # print(first_half)
    second_half = extract_section((row + 1, 0), (height, width), datalist, 1)
    # print('############')
    # print(second_half)

    return first_half, second_half


def lists_sum(datalist1=list(), datalist2=list(), headings=False, new_headings=(None)):
    """Sum of two lists of the same size, heading of datalist 1 is preserved. Otherwise use new_headings type:list[list]
    :param headings: if the file has headings put True in order to avoid sum not numbers
    :param new_headings: new_headings=new value for heading
    :type datalist1: list
    :type datalist2: list
    :type new_headings: list[list]
    """
    if headings is True:
        working_values1 = split_section_row_reference(0, datalist1)
        working_values2 = split_section_row_reference(0, datalist2)

        array1 = np.array(working_values1[1], dtype=np.float)
        array2 = np.array(working_values2[1], dtype=np.float)

        array1 = array1 + array2

        if new_headings is None:
            return np.append(working_values1[0], array1, axis=0).tolist()  # type: list
        else:
            return np.append(new_headings, array1, axis=0).tolist()  # type: list
    else:
        if isinstance(datalist1, type(list())):
            array1 = np.array(datalist1, dtype=np.float)
            array2 = np.array(datalist2, dtype=np.float)
            sum_arrays = array1 + array2
            return sum_arrays.tolist()  # type: list

        elif isinstance(datalist1, type(np.array())):
            sum_arrays = datalist1 + datalist2
            return sum_arrays.tolist()  # type: list


def list_substract(datalist1=list(), datalist2=list(), headings=False, new_headings=(None)):
    """subtract of two lists of the same size"""

    if headings is True:
        working_values1 = split_section_row_reference(0, datalist1)
        working_values2 = split_section_row_reference(0, datalist2)

        array1 = np.array(working_values1[1], dtype=np.float)
        array2 = np.array(working_values2[1], dtype=np.float)

        array1 = array1 - array2

        if new_headings is None:
            return np.append(working_values1[0], array1, axis=0).tolist()  # type: list
        else:
            return np.append(new_headings, array1, axis=0).tolist()  # type: list

    else:

        if isinstance(datalist1, type(list())):
            array1 = np.array(datalist1, dtype=np.float)
            array2 = np.array(datalist2, dtype=np.float)
            sum_arrays = array1 - array2
            return sum_arrays.tolist()  # type: list

        elif isinstance(datalist1, type(np.array())):
            sum_arrays = datalist1 - datalist2
            return sum_arrays.tolist()  # type: list


def lists_make_cero(datalist=list(), headings=False):
    """Sum of two lists of the same size"""
    if headings is True:
        working_values = split_section_row_reference(0, datalist)

        array1 = np.array(working_values[1], dtype=np.float)
        array2 = np.array(working_values[1], dtype=np.float)

        array1 = array1 - array2

        return np.append(working_values[0], array1, axis=0).tolist()

    else:

        if isinstance(datalist, type(list())):
            array1 = np.array(datalist, dtype=np.float)
            array2 = np.array(datalist, dtype=np.float)
            sum_arrays = array1 - array2
            return sum_arrays.tolist()
        # Review if error occurs
        if isinstance(datalist, type(np.array)):
            array1 = np.array(datalist, dtype=np.float)
            array2 = np.array(datalist, dtype=np.float)
            sum_arrays = array1 - array2
            return sum_arrays.tolist()



def coords_dist_col_references(refvalues=('xi', 'xf'), datalist=list(), init_row=0):
        xi = coord_search_full_list_row(refvalues[0], datalist, init_row, 0, False)
        xf = coord_search_full_list_row(refvalues[1], datalist, init_row, 0, False)

        return xf[1] - xi[1]


def list_remove_section_col_references(excluded_list=list(), datalist=list(), return_only_section=False,
                                       remove_nan=True):
    """Return the complete lists of list with the excluded elements in excluded lists. Required: if only one element ['element']
    if retunr_only_section is True, a list with the splits is returned. remove_nan deletes all nan result in the split
    for better performance, if the list is big set remove_nan to False.
     """
    width = len(datalist[0]) - 1  # index 0
    xi = extract_section((0, 0), (0, 0), datalist)[0][0]
    xf = extract_section((0, width), (0, width), datalist)[0][0]
    init_row = 0
    # datalist2 = lists_make_cero(datalist, True)

    # only if there is values to exclude
    if excluded_list is not None:
        # list to store the extraction of the data
        extract_sections_list = []

        # only one value
        # print("len(excluded_list): ", len(excluded_list))
        if len(excluded_list) == 1:

            # tuple with (init ref, end ref, (excluded list offset), [Excluded Range])
            extract_sections_list = [(xi, excluded_list[0], ((-1, 0), (-1, 0)), [excluded_list[0], None]),
                                     (excluded_list[0], xf, ((0, 1), (0, 1)),
                                      [None, None])]
        # Two or more values
        else:

            init_offset = [[-1, 0], [-1, 0]]  # values to avoid sum xf, as xf is excluded
            end_offset = [[0, 1], [0, 1]]  # values to offset xf in 1 unit to right in init as xf is excluded
            middle_offset = [(0, 1), (-1, 0)]  # sum 1 to right to the init and subtract 1 to the lef to the end
            exclude_ref = None  # value used to attach at the end of [Excluded Range]
            new_exclude_ref = None  # used to iterate in the excluded_list
            new_value = False  # check if a contiguous value exist in the middle sections

            for index, item in enumerate(excluded_list):
                if index == len(excluded_list) - 1:  # if the next value is the end, finish -> avoid out or range.
                    extract_sections_list.append((item, xf, end_offset, [None, None]))  # last attach
                    # print_list(extract_sections_list)  # sum references.
                    break

                # compute dist to the next excluded list
                # print("item: ", item)
                # print("excluded_list[index + 1]: ", excluded_list[index+1])
                # print("datalist: ", datalist)
                next_dist = coords_dist_col_references((item, excluded_list[index + 1]), datalist, 0)

                # init case
                if index == 0:

                    # check if contiguous references exists.
                    if next_dist == 1:
                        """if the next value is contiguous the new excluded value is the next from index,
                        then an iteration of the remaining items is done to check if the next value is
                        contiguous, the last contiguous value is stored in exclude_ref"""
                        exclude_ref = excluded_list[index + 1]
                        for value in range(index, len(excluded_list) - 1):
                            next_dist = coords_dist_col_references((excluded_list[value], excluded_list[value + 1]),
                                                                   datalist, 0)
                            if next_dist == 1:
                                exclude_ref = excluded_list[value + 1]
                            else:
                                break

                    # xi -> init value, excluded_list[0] -> end value of first section
                    # init_offset -> no use excluded_list[0] in the sum
                    # [excluded_list[0], exclude_ref] -> range of excluded lists

                    """Append to extract_section_list"""
                    extract_sections_list = [
                        (xi, excluded_list[index], init_offset, [excluded_list[index], exclude_ref])]
                    new_exclude_ref = exclude_ref  # set next value to iterate
                    exclude_ref = None  # return to default value

                # iterate index to the current value.
                if item != new_exclude_ref:
                    continue
                else:

                    if next_dist == 1:
                        new_value = True  # a new contiguous value is found
                        exclude_ref = excluded_list[index + 1]
                        for value in range(index, len(excluded_list) - 1):
                            next_dist = coords_dist_col_references((excluded_list[value], excluded_list[value + 1]),
                                                                   datalist, 0)
                            if next_dist == 1:
                                exclude_ref = excluded_list[value + 1]
                            else:
                                break

                    extract_sections_list.append((new_exclude_ref, excluded_list[index + 1], middle_offset,
                                                  [excluded_list[index + 1], exclude_ref]))

                    new_exclude_ref = excluded_list[index + 1]  # ensure next loop executes

                    if new_value is True:
                        new_exclude_ref = exclude_ref
                        new_value = False

                    exclude_ref = None
        ####################################
        # values before xi and xf section
        first_split = split_section_col_references(xi, datalist, True, init_row=init_row, first_half_offset=-1,
                                                   second_half_offset=0)

        # working_values[0] contains desired section
        # working_values[1] contains the data after xi and xf
        working_values = split_section_col_references(xf, first_split[1], True, init_row=init_row, first_half_offset=0,
                                                      second_half_offset=1)

        working_datalist = working_values[0][:]

        # list of sections
        list_of_sections = []
        # list for  all values, including first_split[0]
        buffer_full_data = []

        if return_only_section is False:
            buffer_full_data = np.array(first_split[0])

        # extract_section_list = (init ref, end ref, (excluded list offset), [Excluded Range])
        for value in extract_sections_list:
            init = value[0]
            end = value[1]
            offset = value[2]
            excluded_range = value[3]

            buffer = __list_remove_section_col_references_aux(init, end, working_datalist,
                                                           init_row, offset, True)

            if return_only_section is False:
                buffer_full_data = np.append(buffer_full_data, buffer, axis=1).tolist()


            # use if return only section is true:
            else:
                # if buffer return empty values, don't append
                if len(buffer[0]) == 0:
                    pass
                else:
                    list_of_sections.append(buffer)

        if return_only_section is True:
            if remove_nan is True:
                list_of_sections = [[None if value == 'nan' else value for value in row]
                                    for row in list_of_sections]
            return list_of_sections
        else:
            if remove_nan is True:
                buffer_full_data = [[None if value == 'nan' else value for value in row]
                                    for row in buffer_full_data]
            return buffer_full_data


def __list_remove_section_col_references_aux(xi='', xf='', datalist1=list(), init_row=0,
                                                         offset=((-1, 0), (0, 1)), return_only_section=False):


    """"Auxiliar method, offset((-1, 0) (0, 1)) means xf included in first split, return_only_section False means
    return the complete array, put True if only xi and xf col section is desired to be returned"""
    # fsplit_offset_2 and ssplit_offset_1 gives the references to sum.
    fsplit_offset_1 = offset[0][0]  # offset from xi -> -1: means empty list in first split [first split]
    fsplit_offset_2 = offset[0][1]  # offset from xi -> 0: means xi is taken as the first part [second split]
    ssplit_offset_1 = offset[1][0]  # offset from xf -> 0: means xf is included as the end point [second split]
    ssplit_offset_2 = offset[1][1]  # offset from xf -> 1: means offset for the third split [third split]

    empty_end_column = False

    # print(" Inside __list")
    # print_list(datalist1)
    # print(row_search_index_data_2dlist(xf, datalist1, init_row) + 1)

    if len(datalist1[0]) == row_search_index_data_2dlist(xf, datalist1, init_row) + 1:
        empty_end_column = True

    #########################################
    if return_only_section is True:
        working_datalist = extract_section_col_references(xi, xf, datalist1, len(datalist1) - init_row, True, init_row,
                                                          0, fsplit_offset_2, ssplit_offset_1)
        # print("xi: ", xi, " xf: ", xf)
        # print("datalist1")
        # print_list(datalist1)
        # print("working_datalist")
        # print_list(working_datalist)
        working_section = split_section_row_reference(init_row, working_datalist)

        # working_section[0] -> headings
        # lists_sum -> Sum values avoiding headings

        # print("print_list")
        # print_list(np.append(working_section[0], lists_sum(working_section[1], list_to_sum), axis=0).tolist())

        return np.append(working_section[0], working_section[1], axis=0).tolist()


def list_append(datalist1=list(), datalist2=list(), reverse=False):
    """append two list of lists, reverse means datalist2 is first, datalist1 otherwise"""
    if reverse is False:
        return np.append(datalist1, datalist2, axis=1)
    if reverse is True:
        return np.append(datalist2, datalist1, axis=1)


def list_merge_col_references(references = list(), datalist=list(), new_name=None, headings=True):
    """Recieves a list with the references and merge in the first."""
    # todo: finish for cases not equal to two
    if len(references) == 2:
        add_list1 = extract_col_reference(references[0], datalist, len(datalist), headings, 0, 0)
        add_list2 = extract_col_reference(references[1], datalist, len(datalist), headings, 0, 0)

        if new_name is not None:
            add_list = lists_sum(add_list1, add_list2, headings, [[new_name]])  # type: list
        else:
            add_list = lists_sum(add_list1, add_list2, headings)  # type: list

        working_coord = coord_search_full_list_row(references[0], datalist, 0, 0, False)

        new_list = list_remove_section_col_references([references[0], references[1]], datalist, False)
        new_list = list_insert_section_col_reference(working_coord, -1, new_list, add_list, True)  # type: list


        print_list(new_list, True)

        return new_list

    return 0


def list_insert_section_col_reference(xi='', offset=0, datalist=list(), insert_list=list(), xi_coords=False):
    """inserts at the right of xi, modify with offset, xi_coords set to True allows to pass coords instead xi ref"""
    working_values = split_section_col_references(xi, datalist, True, 0, 0, 0, offset, 1 + offset, xi_coords)
    array1 = np.append(np.append(working_values[0], insert_list, axis=1), working_values[1], axis=1).tolist()
    return array1


def list_sum_section_col_references(refwords=('xi', 'xf'), datalist1=list(), datalist2=list(), excluded_list=(None),
                                    init_row=0, return_only_section=False):
    """Return the complete lists of list with datalist2 added. if only one is desired to add just refwords='ref'
    :param excluded_list: Values to exclude
    """

    # special case if only xi is given
    if len(refwords) == 1:
        xi = refwords
        xf = xi
    else:
        xi = refwords[0]
        xf = refwords[1]

    # only if there is values to exclude
    if excluded_list is not None:
        # list to store the extraction of the data
        extract_sections_list = []

        # only one value
        if len(excluded_list) == 1:

            # tuple with (init ref, end ref, (excluded list offset), [Excluded Range])
            extract_sections_list = [(xi, excluded_list[0], ((-1, 0), (-1, 0)), [excluded_list[0], None]),
                                     (excluded_list[0], xf, ((0, 1), (0, 1)),
                                      [None, None])]
        # Two or more values
        else:

            init_offset = [[-1, 0], [-1, 0]]  # values to avoid sum xf, as xf is excluded
            end_offset = [[0, 1], [0, 1]]  # values to offset xf in 1 unit to right in init as xf is excluded
            middle_offset = [(0, 1), (-1, 0)]  # sum 1 to right to the init and subtract 1 to the lef to the end
            exclude_ref = None  # value used to attach at the end of [Excluded Range]
            new_exclude_ref = None  # used to iterate in the excluded_list
            new_value = False  # check if a contiguous value exist in the middle sections

            for index, item in enumerate(excluded_list):
                if index == len(excluded_list) - 1:  # if the next value is the end, finish -> avoid out or range.
                    extract_sections_list.append((item, xf, end_offset, [None, None]))  # last attach
                    print_list(extract_sections_list)  # sum references.
                    break

                # compute dist to the next excluded list
                next_dist = coords_dist_col_references((item, excluded_list[index + 1]), datalist1, 0)

                # init case
                if index == 0:

                    # check if contiguous references exists.
                    if next_dist == 1:
                        """if the next value is contiguous the new excluded value is the next from index,
                        then an iteration of the remaining items is done to check if the next value is
                        contiguous, the last contiguous value is stored in exclude_ref"""
                        exclude_ref = excluded_list[index + 1]
                        for value in range(index, len(excluded_list) - 1):
                            next_dist = coords_dist_col_references((excluded_list[value], excluded_list[value + 1]),
                                                                   datalist1, 0)
                            if next_dist == 1:
                                exclude_ref = excluded_list[value + 1]
                            else:
                                break

                    # xi -> init value, excluded_list[0] -> end value of first section
                    # init_offset -> no use excluded_list[0] in the sum
                    # [excluded_list[0], exclude_ref] -> range of excluded lists

                    """Append to extract_section_list"""
                    extract_sections_list = [(xi, excluded_list[index], init_offset, [excluded_list[index], exclude_ref])]
                    new_exclude_ref = exclude_ref  # set next value to iterate
                    exclude_ref = None  # return to default value

                # iterate index to the current value.
                if item != new_exclude_ref:
                    continue
                else:

                    if next_dist == 1:
                        new_value = True  # a new contiguous value is found
                        exclude_ref = excluded_list[index + 1]
                        for value in range(index, len(excluded_list) - 1):
                            next_dist = coords_dist_col_references((excluded_list[value], excluded_list[value + 1]),
                                                                   datalist1, 0)
                            if next_dist == 1:
                                exclude_ref = excluded_list[value + 1]
                            else:
                                break

                    extract_sections_list.append((new_exclude_ref, excluded_list[index + 1], middle_offset,
                                                 [excluded_list[index + 1], exclude_ref]))

                    new_exclude_ref = excluded_list[index + 1]  # ensure next loop executes

                    if new_value is True:
                        new_exclude_ref = exclude_ref
                        new_value = False

                    exclude_ref = None
        ####################################
        # values before xi and xf section
        first_split = split_section_col_references(xi, datalist1, True, init_row=init_row, first_half_offset=-1,
                                                   second_half_offset=0)

        # working_values[0] contains desired section
        # working_values[1] contains the data after xi and xf
        working_values = split_section_col_references(xf, first_split[1], True, init_row=init_row, first_half_offset=0,
                                                      second_half_offset=1)

        working_datalist = working_values[0][:]

        # list of sections
        list_of_sections = []
        # list for  all values, including first_split[0]
        buffer_full_data = []

        if return_only_section is False:
            buffer_full_data = np.array(first_split[0])

        # extract_section_list = (init ref, end ref, (excluded list offset), [Excluded Range])
        for value in extract_sections_list:
            init = value[0]
            end = value[1]
            offset = value[2]
            excluded_range = value[3]

            buffer = __list_sum_section_col_references_aux(init, end, working_datalist, datalist2,
                                                           init_row, offset, True)

            if return_only_section is False:
                buffer_full_data = np.append(buffer_full_data, buffer, axis=1).tolist()

                # only append if there is a value in excluded list.
                if excluded_range[0] is not None:
                    excluded_value = extract_section_col_references(excluded_range[0], excluded_range[1],
                                                           datalist1, len(datalist1) - init_row, True, init_row)

                    buffer_full_data = np.append(buffer_full_data, excluded_value, axis=1).tolist()

            # use if return only section is true:
            else:
                # if buffer return empty values, don't append
                if len(buffer[0]) == 0:
                    pass
                else:
                    list_of_sections.append(buffer)

        if return_only_section is True:
            return list_of_sections
        else:
            return buffer_full_data

    else:
        return __list_sum_section_col_references_aux(xi, xf, datalist1, datalist2, init_row,
                                                     return_only_section=return_only_section)


def list_sum_section_col_reference(refword='', datalist1=list(), datalist2=list(), init_row=0):

    return __list_sum_section_col_references_aux(refword, refword, datalist1, datalist2, init_row)


def __list_sum_section_col_references_aux(xi='', xf='', datalist1=list(), datalist2=list(), init_row=0,
                                          offset=((-1, 0), (0, 1)), return_only_section=False):
    """"Auxiliar method, offset((-1, 0) (0, 1)) means xf included in first split, return_only_section False means
    return the complete array, put True if only xi and xf col section is desired to be returned"""
    # fsplit_offset_2 and ssplit_offset_1 gives the references to sum.
    fsplit_offset_1 = offset[0][0]  # offset from xi -> -1: means empty list in first split [first split]
    fsplit_offset_2 = offset[0][1]  # offset from xi -> 0: means xi is taken as the first part [second split]
    ssplit_offset_1 = offset[1][0]  # offset from xf -> 0: means xf is included as the end point [second split]
    ssplit_offset_2 = offset[1][1]  # offset from xf -> 1: means offset for the third split [third split]

    empty_end_column = False

    # print(" Inside __list")
    # print_list(datalist1)
    # print(row_search_index_data_2dlist(xf, datalist1, init_row) + 1)

    if len(datalist1[0]) == row_search_index_data_2dlist(xf, datalist1, init_row) + 1:
        empty_end_column = True

    #########################################
    if return_only_section is True:

        working_datalist = extract_section_col_references(xi, xf, datalist1, len(datalist1) - init_row, True, init_row,
                                                          0, fsplit_offset_2, ssplit_offset_1)
        # print("xi: ", xi, " xf: ", xf)
        # print("datalist1")
        # print_list(datalist1)
        # print("working_datalist")
        # print_list(working_datalist)
        working_section = split_section_row_reference(init_row, working_datalist)
        list_to_sum = extract_section_col_references(xi, xf, datalist2, len(datalist2) - init_row, False, init_row,
                                                     0, fsplit_offset_2, ssplit_offset_1)

        # print(type(working_section[1]))
        # working_section[0] -> headings
        # lists_sum -> Sum values avoiding headings

            # print("print_list")
            #print_list(np.append(working_section[0], lists_sum(working_section[1], list_to_sum), axis=0).tolist())

        return np.append(working_section[0], lists_sum(working_section[1], list_to_sum), axis=0).tolist()

    else:
        # Get first part
        split1 = split_section_col_references(xi, datalist1, True, 0, 0, 0, fsplit_offset_1, fsplit_offset_2)
        # Get middle and end part
        split2 = split_section_col_references(xf, split1[1], True, 0, 0, 0, ssplit_offset_1, ssplit_offset_2)

        print("first part:")
        for line in split1[0]:
            print(line)
        print("second part:")
        for line in split2[0]:
            print(line)
        print("third part:")
        for line in split2[1]:
            print(line)

        # Extract Headings of middle section
        working_section = split_section_row_reference(init_row, split2[0])
        print("working section:")
        for line in working_section:
            print(line)


        # Extract from second list
        list_to_sum = extract_section_col_references(xi, xf, datalist2, len(datalist2), False, init_row,
                                                     0, fsplit_offset_2, ssplit_offset_1)
        print("list_to_sum")
        print_list(list_to_sum)



        # Sum the desired values
        working_section_sum = lists_sum(working_section[1], list_to_sum)

        # Reattach the heading and section one and three
        new_working_section = np.append(working_section[0], working_section_sum, axis=0)

        buffer = np.append(np.array(split1[0]), new_working_section, axis=1)

        # If empty end column, avoid append.
        if empty_end_column is True:
            pass
        else:
            buffer = np.append(buffer, split2[1], axis=1)

        # update values
        new_data = buffer.tolist()

        return new_data


def print_list(list_of_list=list(), separator=False):
    if separator is True:
        print("##########################")

        for line in list_of_list:
            print(line)

        # print("##########################")
    else:
        for line in list_of_list:
            print(line)


if __name__ == '__main__':

    # Test datalist
    datalist = [
        [None, None, None, 'Edison Chouest Offshore Mexico Services, S. de R. L. de C. V.', None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, 'Av. Los Pinos No. 73, Colonia Playa Norte, C. P. 24198, Cd. Del Carmen Camp', None,
         None, None,
         70.1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, 'R. F. C. ECO040213EMA', None, 'IMSS: A1124295102', None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, 'formula', None, None,
         None, None, None,
         None, None, None, None, None, None],
        [None, None, None, 'Calculo de Nomina Catorcenal Stim Star del 15/02/2016 al  25/02/2016', None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None,
         -2146826265, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Datos', None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None],
        [None, 'N   O   M    B    R    E', 'Barco', 'REG.', 'RFC', 'CURP', 'CARGO O', 'DIAS', 'DIAS', 'Salario',
         'SUELDO',
         'Salary', 'One Week', 'Overtime', 'Overtime Double', 'Overtime Triple', 'Sunday Prime', 'Sunday Prime',
         'Wait and Guard', 'Traveling', 'PREMIOS', 'PREMIOS', 'Food', 'Transporte', 'Monto de ', None, 'TOTAL',
         None, 'BASE',
         'BASE', 'I.S.R. S/Salarios', 'I.M.S.S.', 'CRED.', 'Descto.', 'Descto.', 'NETO  A', 'Dia de', None,
         None], [None, None, None, 'IMSS', None, None, 'PUESTO', 'TRAB', 'FESTIVOS', 'Integrado IMSS', 'DIARIO',
                 'Two Weeks', 'Salary',
                 'Not Taxable', 'Taxable', 'Taxable', 'Not Taxable', 'Taxable', 'Relieve per Ship', 'Meal',
                 'X PUNT.', 'X ASIST.',
                 'Basket', None, 'Dias Festivos', None, 'INGRESOS', None, 'I.S.P.T.', 'I.M.S.S.', None, None,
                 'AL SAL.', 'Infonavit',
                 'Alimentacion', 'RECIBIR', 'Pago', None, None],
        [None, 'nombre', 'Barco', None, 'rfc', 'curp', None, 'dt', 'dias_festivos', 'Salario', 'Sal_Diario',
         '2w', '1w', 'hen',
         'he2', 'he3', 'sp', 'spt', 'wgr', 'tm', 'ppa', 'ppp', 'fb', 'trans', 'm_dias_g', 'm_dias_e', None,
         None, None, None,
         'isr', 'imss', None, 'infonavit', 'da', 'total', 'dia_pago', None, None],
        [None, 'Susano Cuellar Y Hernandez', 'Stim Star', 81906708763.0, 'CUHS6710285Y5', 'CUHS671028HVZLRS01',
         'First Mate DP(Capitanl)', 0.0, 0.0, 1826.0000000000002, 1555.4128937077, 19442.66117134625,
         9721.330585673126,
         652.1428571428572, 5597.283947932723, 34371.847427915694, 130.42857142857144, 563.9521846909374,
         382.41071428571433,
         714.3125, 2282.5000000000005, 2282.5000000000005, 547.8000000000001, 160.71428571428572, 1947.93,
         1947.93,
         80745.74424613014, None, 76067.31281755873, 65321.14494105459, 21797.0034449694, 933.6566250000002,
         0.0, 0.0,
         547.8000000000001, 57467.284176160734, '24 Marzo', 57467.27967616075, 0.004499999980907887],
        [None, 'Alfredo Madrid Caballero', 'Stim Star', 65967825111.0, 'MACA7811099I3', 'MACA781109HVZDBL08',
         'First Mate DP(1er. Oficial)', 0.0, 0.0, 0.0, 1256.8608931301953, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 629.894, 629.894, 1259.788, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1259.788,
         '28 Marzo',
         51259.78380799863, -49999.99580799863],
        [None, 'Nely Elizabeth Gonzalez Hernandez', 'Stim Star', 9058692717.0, 'GOHN860812FC2',
         'GOHN860812MVZNRL08',
         'Firs Mate DP (Oficial de Cubierta)', 0.0, 1.5, 0.0, 963.4946712992926, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 724.827675, 724.827675, 1449.65535, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         1449.65535,
         '28 de Marzo', 1449.65535, 0.0],
        [None, 'Edwin Miguel Loaeza Peraza', 'Stim Star', 23048745295.0, 'LOPE870531IJ8', 'LOPE870531HSLZRD8',
         'Deck Hand (Marinero)', 0.0, 0.0, 0.0, 402.7762590859984, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0],
        [None, 'Edgar Steven Carrillo Mendoza', 'Stim Star', 23118820127.0, 'CAME881228RB7',
         'CAME881228HNERND16',
         'Second Enginner', 0.0, 0.0, 0.0, 963.4946712913003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         483.23, 483.23, 966.46, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 966.46, '24 Marzo', 40966.45999041957,
         -39999.99999041957],
        [None, 'Juan Carlos Gutierrez Hernandez', 'Stim Star', 42866675067.0, 'GUHJ670516UJ8',
         'GUHJ670516HDFTRN06',
         'Deck Hand (Marinero)', 0.0, 0.0, 0.0, 402.7762590804504, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         0.0, 201.59230526328463, 201.59230526328463, 403.18461052656926, None, 0.0, 0.0, 0.0, 0.0, 0.0,
         1916.8704799999998,
         0.0, -1513.6858694734306, '24 Marzo', 17635.468938801612, -19149.15480827504],
        [None, 'Alejandro Alberto Leon Recio', 'Stim Star', 84028313637.0, 'LERA8304028X9',
         'LERA830402HYNNCL08',
         'Motorman (Motorista)', 0.0, 0.0, 0.0, 402.77625909089676, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         0.0, 201.59230526328463, 201.59230526328463, 403.18461052656926, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0,
         403.18461052656926, '28 Marzo', 19552.33941920584, -19149.15480867927],
        [None, 'Jaime Gabino Mulato', 'Stim Star', 83856705294.0, 'GAMJ740905GX0', 'GOGM670418HTCNNR01',
         'Deck Hand (Marinero)',
         0.0, 0.0, 165.92610190952917, 231.42878545216527, 925.7151418086611, 462.85757090433054,
         208.6857142857143,
         88.86558129564105, 1636.5321256974546, 33.06125506459504, 0.0, 48.871428571428574, 228.58,
         232.29654267334087,
         232.29654267334087, 175.29600000000002, 51.42857142857143, 0.0, 0.0, 4324.486474403079, None,
         4082.739505052769,
         3333.762093475041, 653.2879031779017, 91.43455588777815, 0.0, 386.32109999999994, 175.29600000000002,
         3018.1469153373996, '28 Marzo', 3018.1469153373996, 0.0],
        [None, 'Jose Adrian Cancino Dzul', 'Stim Star', 9058017549.0, 'CADA800513L97', 'CADA800513HTSNZDU4',
         'Deck Hand (Marinero)', 0.0, 0.0, 580.7413566349081, 231.4287854311204, 3240.0029960356856,
         1620.0014980178428,
         730.4000000000001, 311.0295344400415, 5727.86243942023, 115.7143927155602, 0.0, 171.05,
         800.0300000000001,
         813.0378992888714, 813.0378992888714, 613.5360000000001, 180.0, 115.66305164364884, 115.66305164364884,
         15367.028762494398, None, 14289.588266491543, 11668.167326189316, 2286.507660867799, 320.0209455789927,
         0.0, 0.0,
         613.5360000000001, 12146.964156047605, '28 Marzo', 12146.964156047605, 0.0],
        [None, 'Alvaro Muñoz Lopez', 'Stim Star', 78078206709.0, 'LOMA820419HR2', 'LOMA820419HOCPXL00',
         'First Mate DP(1er. Oficial)', 0.0, 0.0, 518.5190684200749, 231.4287854291983, 2892.859817864979,
         1446.4299089324895,
         652.1428571428572, 277.7049414566003, 5114.162892297016, 103.31642206660638, 0.0, 152.7232142857143,
         714.3125,
         725.9266957881048, 725.9266957881048, 547.8000000000001, 160.71428571428572, 289.1576291091221,
         289.1576291091221,
         14092.335489555, None, 12758.560952127293, 10418.00654116109, 2041.5246971826089, 285.73298712231707,
         0.0, 0.0,
         547.8000000000001, 11217.277805250074, '28 Marzo', 11217.277805250074, 0.0],
        [None, 'Total', None, None, None, None, None, None, None, None, None, 26501.239127055574,
         13250.619563527787,
         2243.371428571429, 6274.884005125005, 46850.4048853304, 382.52064127533305, 563.9521846909374,
         755.0553571428572,
         2457.235, 4053.761137750317, 4053.761137750317, 1884.4320000000002, 552.8571428571429, None, None,
         119011.86754363577,
         None, 107198.20154123034, 90741.08090188004, 26778.32370619771, 1630.8451135890882, 0.0,
         2303.1915799999997,
         1884.4320000000002, 86415.07514384895, None, 214713.3760592215, -128298.30091537254],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, 69759.67, None, None, None, 4163.94, None,
         None,
         128298.30091537256, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, -42981.346293802286, None, None, None,
         -2279.5079999999994,
         None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         205525.6439472842, None,
         None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         -119110.56880343525, None,
         None, None]]

    # search for coords to extract values
    values_search = coord_search_xiyi_xfyf("nombre", "dia_pago", "Total", datalist, 0, 0)

    working_values = extract_section(values_search[0], offset_coords(values_search[1], -1), datalist)
    print_list(working_values)

    add_list1 = extract_col_reference("m_dias_g", working_values, len(working_values), True, 0, 0)
    add_list2 = extract_col_reference("m_dias_e", working_values, len(working_values), True, 0, 0)

    add_list = lists_sum(add_list1, add_list2, True)  # type: list

    working_coord = coord_search_full_list_row("m_dias_g", working_values, 0, 0, False)

    new_list = list_remove_section_col_references(["m_dias_g", "m_dias_e"], working_values, False)
    new_list = list_insert_section_col_reference(working_coord, -1, new_list, add_list, True)  # type: list

    print_list(new_list, True)

    new_list2 = list_merge_col_references(["m_dias_g", "m_dias_e"], working_values, "Dias_Festivos")

    import xlwings as xl
    wb = xl.Workbook()

    xl.Range("B2").value = new_list2




