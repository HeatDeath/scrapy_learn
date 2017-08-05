"""
可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple
关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
"""

# 可变参数，传入参数的个数是可变的
def clac(*args):
    my_sum = 0
    print(args)
    for n in args:
        my_sum += n
    print(my_sum)

clac(1, 2)
clac(1, 2, 3)

# *nums 表示把 nums 这个 list 的所有元素作为可变参数传进去
clac(*[1, 2, 3])
clac(*(1, 2, 3))

# --------------------------------------------

# 关键字参数
def counter(**kwargs):
    my_sum = 0
    print(kwargs)
    for n in kwargs.values():
        my_sum += n
    print(my_sum)

counter(A=6, B=1, C=3)

# **extra表示把extra这个dict的所有key-value用关键字参数传入到函数的**kw参数
# kw将获得一个dict，注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra。
counter(**{'A': 6, 'B': 1, 'C': 3})