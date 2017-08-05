class MethodTest(object):
    def __init__(self, input_string):
        self.my_string = input_string

    def normalMethod(self):
        print('this is normal method ---- {}'.format(self.my_string))

    @classmethod
    def classMethod(cls, kkk):
        # print('class method', cls)
        method_test_instance = cls(kkk.split()[0])
        print('this is the usage of classmethod ! you can see it !!! ---- {}'.format(method_test_instance.my_string))
        print(type(method_test_instance))

    @staticmethod
    def staticMethod():
        print('this is static method')

my_test = MethodTest('hello world')
print(type(my_test))
my_test.normalMethod()

MethodTest.classMethod('hello world')

MethodTest.staticMethod()

#
#
# class Date(object):
#
#     def __init__(self, day=0, month=0, year=0):
#         self.day = day
#         self.month = month
#         self.year = year
#
#     @classmethod
#     def from_string(cls, date_as_string):
#         day, month, year = map(int, date_as_string.split('-'))
#         date1 = cls(day, month, year)
#         return date1
#
#     @staticmethod
#     def is_date_valid(date_as_string):
#         day, month, year = map(int, date_as_string.split('-'))
#         return day <= 31 and month <= 12 and year <= 3999
#
#
# date2 = Date.from_string('11-09-2012')
# print(date2)
# print(type(date2))
#
# # usage:
# is_date = Date.is_date_valid('11-09-2012')
# print(is_date)
# print(type(is_date))