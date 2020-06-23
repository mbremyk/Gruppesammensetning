import openpyxl as opxl
from tkinter.filedialog import askopenfilename

if __name__ == '__main__':
    filename = askopenfilename()
    print(filename)
    wb = opxl.load_workbook(filename)
    print(wb.sheetnames)