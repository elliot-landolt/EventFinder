
from pprint import pprint

from app.database.db import service

# this is used to test database connection

if __name__ == "__main__":

    print("---------------")
    print("SPREADSHEET SERVICE...")
    print("DOCUMENT:", service.document_id)

    print("SHEETS:")
    sheets = service.sheets
    for sheet in sheets:
        #print(type(sheet)) #> <class 'gspread.worksheet.Worksheet'>
        print("...", sheet)

    sheet_name = input("Please choose a sheet name: ") or sheets[0].title
    print(sheet_name)
    sheet = service.get_sheet(sheet_name)

    records = sheet.get_all_records()
    print("RECORDS:")
    print(len(records))
    for record in records:
        print("-----")
        pprint(record)