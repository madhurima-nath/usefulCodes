# get necessary libraries
import requests
import io
import datetime
import PyPDF2
import re
import pandas as pd
from bs4 import BeautifulSoup


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


def get_text_from_ordered_list(url):
    """
    extracts text from ordered lists
    on a webpage
    """
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    paragraph = []
    for p in soup.find_all("p"):
        paragraph.append(p.get_text().strip())

    ordered_lists = soup.find_all("ol")

    text_list = []
    for ol in ordered_lists:
        for li in ol.find_all("li"):
            text_list.append(li.get_text().strip())

    return paragraph, text_list


def get_pdf_contents(url, search_text):
    """
    this function extracts a section
    of text, `search_text` from a pdf
    document provided using a link
    """
    response = requests.get(url)
    if response.status_code == 200:
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            lines = text.split("\n")

        for i, line in enumerate(lines):
            if line in search_text:
                paragraph = search_text + " "
                j = i + 1
                while j < len(lines) and not lines[j].startswith(" "):
                    paragraph += lines[j] + " "
                    j += 1
                return paragraph.strip()
        
        return None


def get_updates(df, country):
    """
    get all updates - links, dates,
    topics, sub-topics etc. 
    """
    # filter dataframe for country
    df_country = df[df["country"] == country]
    df_country.reset_index(drop=True, inplace=True)

    # create a dict containing all necessary details
    # url_index = df_country["cell_value"].loc[df_country["updated_link"] == True].index.tolist()

    output = {}
    temp, temp_date, temp_text, temp_url, prev_col1, prev_col2 = [], [], [], [], [], []

    for i in range(len(df_country)):
        country = df_country.loc[i, "country"]

        # get contents of previous columns
        if df_country.loc[i, "adj_prev_col1"]:
            prev_col1 = df_country.loc[i, "adj_prev_col1"]
        if df_country.loc[i, "adj_prev_col2"]:
            prev_col2 = df_country.loc[i, "adj_prev_col2"]

        # get updated dates
        # get updated dates if in datetime format
        # if type(df_country.loc[i, "cell_value"]) == datetime.datetime:
            # temp_date.append(df_country.loc[i, "cell_value"].strftime("%Y-%m-%d"))
        if ( ("date" in (df_country.loc[i, "excel_comments"]))
            and (df_country.loc[i, "update_text"]) 
            and ("Updates" not in df_country.loc[i, "column_header"]) ):
            temp_date.append(df_country.loc[i, "update_text"])

        # get updated urls
        if ( (df_country.loc[i, "updated_link"] == True)
            and (check_url(df_country.loc[i, "cell_value"]) == True) ):
            temp_url.append(df_country.loc[i, "cell_value"])

        # get search text in pdfs (if any)
        if ("Updates" in df_country.loc[i, "column_header"]):
            temp_text.append(df_country.loc[i, "update_text"])

        # get comments
        temp.append(df_country.loc[i, "comments"])
        temp_comments = list(set(temp))[0]

        if country not in output:
            output[country] = {"country": country, 
                                "url": temp_url,
                                "prev_col1": prev_col1,
                                "prev_col2": prev_col2,
                                "header": temp_text,
                                "comments": temp_comments,
                                "date": temp_date}
    return output