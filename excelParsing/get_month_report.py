# get necessary libraries
import pandas as pd
import openpyxl
import datetime
import numpy as np
import re


def check_url(string):
    """
    findall() used with the conditions
    which is valid for url in the string
    """
    regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9afA-F]))+"
    URL = re.findall(regex, string)
    if URL:
        return True
    else:
        return False


## parse excel file
def parse_excel(filename):
    """
    this function takes the excel file
    and parses it to extract the cell values
    where there is an update/change
    mentioned in the excel comments
    and/or hyperlinks in red.
    this will not work if
    - hyperlinks are not in red (RGB value is hard coded)
    - there are no excel comments added to the cells
    if there are updated links not in red,
    but the cell has a comment, the function
    will extrcat the information
    """

    # read excel file
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    # create a dictionary to store all new comments
    comments_dict = {}

    # create a dictionary to store updated hyperlinks (in red)
    hyperlinks_dict = {}

    # get the maximum value for columns
    max_col = sheet.max_column

    for row in sheet.iter_rows(values_only=False):
        for cell in row:
            if cell.comment:
                comments_dict[f"{cell.coordinate}"] = [cell.coordinate,
                                                        sheet.cell(cell.row, 1).value,
                                                        (cell.comment.text.split("\n ")[-1].strip()),
                                                        cell.value,
                                                        sheet.cell(cell.row, cell.column-1).value,
                                                        sheet.cell(cell.row, cell.column-2).value,
                                                        sheet.cell(1, cell.column).value,
                                                        sheet.cell(cell.row, max_col).value]
                # ["cell_id", "country", "excel_comments", "cell_value",
                #    "prev_col_1", "prev_col_2, excel_column_header", "comments"]

                # iterate through cells and extract only those hyperlinks in red
                if cell.font.color:
                    if "rgb" in cell.font.color.__dict__:
                        if cell.font.color.rgb == "FFFF0000": # rgb value for red font color
                            if cell.hyperlink:
                                # print(f"Cell {cell.coordinate} contains hyperlink")
                                hyperlinks_dict[f"{cell.coordinate}"] = cell.hyperlink.target

                # if updated hyperlinks are not in red, but cell has a comment
                # use the following tp get the hyperlinks_dict

                # check if the cell value is a hyperlink
                if ( (type(cell.value) == str)
                    and (check_url(cell.value) == True) ):
                    hyperlinks_dict[f"{cell.coordinate}"] = cell.value

        df = pd.DataFrame(comments_dict.items(), columns=["cell_id", "cell_list"])
        return df, hyperlinks_dict