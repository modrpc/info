import pandas as pd

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

    def print(self, prefix):
        if (self.item_type == '단일상품'):
            print(prefix, self.item_name, ' x', self.item_quantity)
        elif (self.item_type == '조합형옵션상품'):
            print(prefix, self.item_option, ' x', self.item_quantity)

class Order:
    def __init__(self, row):
        self.order_no = int(row['주문번호'])
        self.customer_name = row['구매자명']
        self.recipient_name = row['수취인명']
        self.recipient_addr = str(row['기본배송지']) + ' ' + str(row['상세배송지'])
        self.customer_phone = row['구매자연락처']
        self.recipient_phone1 = row['수취인연락처1']
        self.recipient_phone2 = row['수취인연락처2']
        self.delivery_message = row['배송메세지']
        self.order_items = []

    def print(self):
        print(self.order_no, ':')
        print('\t', self.customer_name, ' (', self.customer_phone, ')')
        print('\t', self.recipient_name, ' (', self.recipient_phone1, ', ',
              self.recipient_phone2, ')')
        print('\t', self.recipient_addr)

    def add_order_item(self, row):
        item = OrderItem(row)
        self.order_items.append(item)
        return item
        
    def get_order_items(self):
        return self.order_items

    def is_canceled(self):
        retval = True
        for item in self.order_items:
            if (not item.is_canceled()):
                retval = False
        return retval

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

filename = '20221030.xlsx'
na_values = 'NaN'

df = pd.read_excel(filename, sheet_name='발주발송관리', skiprows=[0])


dict = OrderDict(df.columns)
#print(df.columns)

for index, row in df.iterrows():
    order_no = int(row['주문번호'])
    #print('**', index, row['주문번호'], row['상품주문번호'])
    if (not dict.contains(order_no)):
        #print(index, row['주문번호'])
        order = dict.insert(order_no, row)
        item = order.add_order_item(row)
        #if (not item.is_canceled()):
        #   order.print()
    else:
        try:
            order = dict.get_order(order_no)
            order.add_order_item(row)
            #print('\tFOUND_ORDER')
        except OrderException:
            print('ERROR: no such order -- ', order_no)
            pass

orders = dict.get_orders()
for key in orders:
    order = orders[key]
    if (order.is_canceled()):
        continue
    order.print()
    items = order.get_order_items()
    for item in items:
        item.print('\t\t')
