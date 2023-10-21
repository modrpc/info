import os
import order
import pandas as pd

testfile = 'tests/test_basic_file.xlsx'

def create_excel_workbook():
    wb = workbook(FileFormatType.XLS)
    return wb

if __name__ == "__main__":
    orderdict = order.build_orders_from(testfile)
    order.dump_orders(orderdict.get_orders())
    npa = order.export_excel(orderdict.get_orders())
    df = pd.DataFrame(npa)
    df.to_excel('a.xls')
    

