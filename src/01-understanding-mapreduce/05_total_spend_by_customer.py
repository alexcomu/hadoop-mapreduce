__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep

# Total Spent By Customer
# File: 05_customer-orders.csv

# Structure:
# customerID, ItemID, OrderAmount
# 44,8602,37.19

class MRTotalSpenDByCustomer(MRJob):
    # Simple example

    def mapper(self, _, line):
        (customerID, itemID, orderAmount) = line.split(',')
        yield customerID, float(orderAmount)

    def reducer(self, customer, orders_amount):
        yield customer, sum(orders_amount)


class MRTotalSpenDByCustomerOrdered(MRJob):
    # Simple example + sort by amounts

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_orders,
                reducer=self.reducer_total_by_customer),
            MRStep(
                mapper=self.mapper_make_amount_as_key,
                reducer=self.reducer_output),
        ]

    # Step 1
    def mapper_get_orders(self, _, line):
        (customerID, itemID, orderAmount) = line.split(',')
        yield customerID, float(orderAmount)

    def reducer_total_by_customer(self, customer, orders_amount):
        yield customer, sum(orders_amount)

    # Step 2
    def mapper_make_amount_as_key(self, customer, total_amount):
        yield '%04.02f' % float(total_amount), customer

    def reducer_output(self, orders_amount, customer):
        for user in customer:
            yield user, orders_amount


if __name__ == '__main__':
    MRTotalSpenDByCustomerOrdered.run()
