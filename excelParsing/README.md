# Create Monthly Word Documents from Excel Reports
This codebase is a framework to parse Excel data
and produce Word document as output. 
The data here is dummy, and do not correspond to actual real data. 

This is intakes the excel reports 
which have information regarding
changes/updates and creates an output Word document.
The Excel file has information on updates made on either on
weblinks or some dates indicating when these changes were
made/effective. In the `\data` folder, there is dummy data
showing data for 3 countries - USA, Canada, Australia, for two
months. Using these monthly Excel reports,
a Word document corresponding to each monthly report
is generated in `\output` folder.


## Process
There are sample monthly reports, June & July as examples.
There are multiple python scripts which parse the information
from Excel. The details of the functions used are described
in section [Python functions used](#python-function-used).


### Steps to identify updates
- Each cell in Excel is checked if there is any entry in red font color
or if there is an Excel comment attached to the cell.
- If the above is true, the corresponding country is identified as
the one which has update(s)/change(s).
- Any dates, links, comments, text in red are collected for these
countries and the initial dataframe is created.
- if there is a certain text that needs to be searched in a pdf
document (this is not the case in the sample data), there is a
function defined to obtain this information. 
*(Note: The final output may need to be formatted correctly, depending on the pdf.)*
- The final output is obtained by parsing the dataframe and 
adding each update to the output Word document.

Note: It is possible that each country has its own way of updating
the weblinks or documents. 

The links in the Word document are not clickable 
(need to update that later).


## Python functions used
This section describes the functions used in the codebase.
- notebook `parse.ipynb`: takes filename as input (Excel files)
and generates the output (Word documents) containing the
updates for countries.

### read monthly reports
- function `parse_excel(filename)`: takes Excel file and
parses it to extract those cell values where there is an
update/change mentioned in excel comments or colored in red.
This will **not** work if hyperlinks are not in red.
(RGB value for red is hard coded. To allow for other
colors, condition has to be changed accordingly.)
- function `process_df(filename)`: processes initial
dataframe obtained from reading the Excel file. Additional
columns are added as needed to capture the updates.
- function `add_update_text_col(df)`: parses different
columns to get updates from excel cells where the updates are
mentioned in the comments numerically. There are multiple
variations of how these could be presented, and to capture
these multiple `if-statements` are used.
- function `extract_previous_col_text(df)`: parses the dataframe
to get information from previous two columns - Topic &
Sub-topic - when these are updated before the date columns.

### get contents from reports
- file `extract_contents.py`: returns a dictionary containing
all relevant information required to be added to the 
Word document.
- function `get_pdf_contents(url, search_text)`: extracts
`search_text` from a pdf linked to a `url`.
- function `get_updates(df, country)`: gets updated weblinks,
dates, information on previous columns etc. for any country
marked in red (i.e., with updates).

### write output document
- file `wite_output.py` contains function to generate output
document.
- function `word_output(df)`: writes the output in a Word document.
