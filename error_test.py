
try:
    fr = open('kkk.txt', 'r')
except Exception as e:
    print(e)
finally:
    print('test end')


print('hello world')

aa = '666'

try:
    print(aa)
except Exception as e:
    print(e)
else:
    print('test end')

fr_kk = open('testfile', 'r')

print('hello world')
