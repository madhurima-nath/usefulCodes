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


