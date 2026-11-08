import urllib.request, json
from pathlib import Path
from openpyxl import load_workbook
R=Path(__file__).parent
for year,uid in [(2025,'b96b9a33-3301-4f17-8eda-9db4d9e8fc4e'),(2024,'3bbefdea-b6fb-461d-97b0-ef20b04abd9f')]:
    f=R/f'singstat-{year}.xlsx'
    if not f.exists(): f.write_bytes(urllib.request.urlopen(f'https://www.singstat.gov.sg/files/{uid}.xlsx').read())
    w=load_workbook(f,read_only=True,data_only=True)
    print(year,w.sheetnames)
    for s in [w.worksheets[0]]:
        print('SHEET',s.title,s.max_row,s.max_column)
        for i,row in enumerate(s.iter_rows(values_only=True)):
            if i<3 or (row[0]=='Hougang' and row[1] in ['Total','Hougang Central'] and row[3]=='Total'):
                print(i,row)
