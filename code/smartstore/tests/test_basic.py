from .context import order

testfile = 'test_basic_file.xlsx'

orders = order.build_orders_from(testfile)

order.dump_orders(orders)

