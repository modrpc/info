import pandas as pd
import numpy as np
import openpyxl

nan_values = ['NaN', 'nan']
debug = False

class OrderException(Exception):
    pass

class OrderItem:
    def __init__(self, row):
        self.item_number = int(row['상품주문번호'])
        self.item_name = row['상품명']
        self.item_type = row['상품종류']
        self.item_option = row['옵션정보']
        self.item_quantity = row['수량']
        self.order_status = row['주문상태']
        self.order_status_detail = row['주문세부상태']

    def number(self):
        return self.item_number
    
    def name(self):
        return self.item_name

    def is_canceled(self):
        if (self.order_status == '취소' and
            self.order_status_detail == '취소완료'):
            return True
        else:
            return False

    def __str__(self):
        s = ''
        if (self.item_type == '단일상품'):
            s =  str(self.item_name + str(self.item_quantity))
        elif (self.item_type == '조합형옵션상품'):
            s = str(self.item_option.strip(' ') + str(self.item_quantity))
        return s

    def print(self, prefix):
        if (self.item_type == '단일상품'):
            print(prefix, self.item_name, ' x', self.item_quantity, sep='')
        elif (self.item_type == '조합형옵션상품'):
            print(prefix, self.item_option, ' x', self.item_quantity, sep='')

class Order:
    def __init__(self, row):
        self.order_no = int(row['주문번호'])
        self.customer_name = row['구매자명'].strip()
        self.recipient_name = row['수취인명'].strip()
        self.recipient_addr = str(row['기본배송지']) + ' ' + str(row['상세배송지'])
        self.customer_phone = str(row['구매자연락처']).strip()
        self.recipient_phone1 = str(row['수취인연락처1']).strip()
        self.recipient_phone2 = str(row['수취인연락처2']).strip()
        self.delivery_message = str(row['배송메세지']).strip()
        self.order_items = []
        self.slist = []

    def print(self):
        print('order#', self.order_no, ':', sep='')
        print('\t', self.customer_name, ' (', self.customer_phone, ')', sep='')
        print('\t', self.recipient_name, ' (', self.recipient_phone1, ', ',
              self.recipient_phone2, ')', sep='')
        print('\t', self.recipient_addr, sep='')
        if (self.delivery_message not in nan_values):
            print('\t', self.delivery_message, sep='')

    def add_order_item(self, row):
        item = OrderItem(row)
        self.order_items.append(item)
        return item
        
    def get_order_items(self):
        return self.order_items

    def str_order_items(self):
        s = ''
        for item in self.order_items:
            s = s + str(item) + ' '
        return s

    def is_canceled(self):
        retval = True
        for item in self.order_items:
            if (not item.is_canceled()):
                retval = False
        return retval

    def to_list(self):
        self.slist.append(self.customer_name)
        self.slist.append(self.recipient_addr)
        self.slist.append(self.recipient_phone1)
        self.slist.append(self.recipient_phone1)
        self.slist.append(1)
        self.slist.append(3650)
        self.slist.append('선불')
        self.slist.append(self.str_order_items())
        msg = '< 꼭 당일배송, 파손주의 > 안정배송부탁드립니다.'
        if (self.delivery_message not in nan_values):
            msg = self.delivery_message + ' ' + msg
            self.slist.append(msg)
        return self.slist

class OrderDict:
    def __init__(self, columns):
        self.dict = {}
        self.columns = columns

    def contains(self, order_no):
        if order_no in self.dict:
            return True
        else:
            return False

    def get_order(self, order_no):
        if self.contains(order_no):
            return self.dict[order_no]
        else:
            raise OrderException()

    def get_orders(self):
        return self.dict

    def insert(self, order_no, row):
        order = Order(row)
        self.dict[order_no] = order
        return order

def build_orders_from(filename):
    df = pd.read_excel(filename, sheet_name='발주발송관리', skiprows=[0])

    dict = OrderDict(df.columns)
    if (debug):
        print(df.columns)

    for index, row in df.iterrows():
        order_no = int(row['주문번호'])
        if (debug):
            print('**', index, row['주문번호'], row['상품주문번호'])
        if (not dict.contains(order_no)):
            if (debug):
                print(index, row['주문번호'])
            order = dict.insert(order_no, row)
            item = order.add_order_item(row)
            if (debug):
                if (not item.is_canceled()): order.print()
        else:
            try:
                order = dict.get_order(order_no)
                order.add_order_item(row)
                if (debug):
                    print('\tFOUND_ORDER')
            except OrderException:
                print('ERROR: no such order -- ', order_no)
                pass

    return dict


def dump_orders(orders):
    for key in orders:
        order = orders[key]
        if (order.is_canceled()):
            continue
        order.print()
        items = order.get_order_items()
        for item in items:
            item.print('\t\t')


def export_excel(orders):
    rows = []
    for key in orders:
        order = orders[key]
        if (order.is_canceled()):
            continue
        l = order.to_list()
        rows.append(l)
    npa = np.array(rows)
    return npa
        

        
