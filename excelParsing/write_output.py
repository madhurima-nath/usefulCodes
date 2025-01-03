# get necessary libraries
import extract_contents
import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import RGBColor


def word_output(df):
    """
    this function writes the output
    to a word document.
    since every country has a different
    input structure, multiple if conditions
    are used to capture these, along with
    a generic section
    """

    # create a new document
    document = Document()

    # get output
    result = {}
    for x in df["country"].unique():
        temp = extract_contents.get_updates(df, x)
        if temp and x not in result:
            result = temp
        try:
            if "pdf" in result[x]["url"][0]:
                url = result[x]["url"][0]
                search_text = result[x]["header"]
                result = extract_contents.get_pdf_contents(url, search_text)
        except:
            print(f"No pdfs updated for {x}. Only updated urls and/or dates.")
            result = temp

        print(result)

        for key, value in result.items():
            # add country as heading
            country = value.get("country")
            heading = document.add_heading(country, level=1)
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
            heading.runs[0].font.color.rgb = RGBColor(255, 0, 0) # red color
            heading.runs[0].font.underline = True # underline

            # start document body
            document.add_paragraph("Updates/Changes:".upper())

            if len(value.get("date")) == len(value.get("url")):
                document.add_paragraph("information on dates, links and previous columns:".upper())
                document.add_paragraph("LINK(S):")
                if len(value.get("url")) > 1:
                    for x in value.get("url"):
                        document.add_paragraph(x)
                else:
                    document.add_paragraph(value.get("url"))
                document.add_paragraph(f"Information in Title column: {value.get('prev_col2')}")
                document.add_paragraph(f"Information in Sub-title column: {value.get('prev_col1')}")
                document.add_paragraph("DATE(S):")
                for x in value.get("date"):
                    document.add_paragraph(x)
                document.add_paragraph("Updated header:".upper())
                if value.get("header") == []:
                    document.add_paragraph("No updated header text.")
                else:
                    document.add_paragraph(value.get("header"))

            else:
                document.add_paragraph("there is a misalignment between updated dates and/or links.".upper())
                document.add_paragraph("or".upper())
                document.add_paragraph("some updates might be for dates only, not links.".upper())
                document.add_paragraph("LINK(S):")
                document.add_paragraph(value.get("url"))
                document.add_paragraph("DATE(S):")
                for x in value.get("date"):
                    document.add_paragraph(x)
                document.add_paragraph("Updated header:".upper())
                if value.get("header") == []:
                    document.add_paragraph("No updated header text.")
                else:
                    document.add_paragraph(value.get("header"))
                

            document.add_paragraph("Comments:".upper())
            document.add_paragraph(f"{value.get('comments')}")

    return document