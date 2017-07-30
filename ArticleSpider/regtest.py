"""
特殊字符
1、 ^ $ * ? + {2} {2,} {2,5} |
2、 [] [^] [a-z] .
3、 \s \S \w \W
4、 [\u4E00-\u9FA5] () \d

"""

import re

# line = 'bobby123'

# . 代表任意字符， * 代表前边的字符出现任意多次
# b 开头，后边任意字符出现任意多次
# re_pattern = '^b.*'
# if re.match(re_pattern, line):
#     print("success!")
# -----------------------------------------

# $ 代表以之前字符结尾
# b 开头，中间任意字符，3 结尾
# re_pattern = '^b.*3$'
# if re.match(re_pattern, line):
#     print("success!")
# -----------------------------------------


# line = 'booooooooooooooooooooobby123'
#
# re_pattern = '.*(b.*b).*'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
#     # bb
#     # 出现此种现象是因为，正则表达式是 反向匹配(从右向左匹配) 的
#
# # ? 代表 非贪婪匹配
#
# re_pattern = '.*?(b.*b).*'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
#     # booooooooooooooooooooobb
#
# re_pattern = '.*?(b.*?b).*'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
#     # booooooooooooooooooooob
# -----------------------------------------

# + 代表 出现至少一次
#
# line = 'booooooooooooooooooooobbbaby123'
# re_pattern = '.*(b.*b).*'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
# -----------------------------------------

# {x} x 表示前面字符出现的次数
# {x,} 大于等于 x
# {x,y} 大于等于 x，但小于等于 y
# line = 'booooooooooooooooooooobbbaaby123'
# re_pattern = '.*(b.{2,}b).*'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
# ----------------------------------------------

# | 表示 或 的关系
# line = 'boobby123'
# re_pattern = '((bobby|boobby)123)'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
# ----------------------------------------------


# # [] 中的任意一个字符出现即可
# line = '18782928569'
#
# # [^1] 代表不等一都可以
# # [] 中的 . * 都没有特殊含义
#
# re_pattern = '(1[48357][0-9]{9})'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))
# ----------------------------------------------


# \s 表示 空格 ， \S 表示 不为空格 都可以

# line = '你 好'
# re_pattern = '(你\S好)'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))

# \w 等于 [A-Za-z0-9_]
# \W 与 \w 的含义相反
# ----------------------------------------------


# re_pattern = '([\u4E00-\u9FA5])'
# match_obj = re.match(re_pattern, line)
# if match_obj:
#     print(match_obj.group(1))


# \d 代表 数字

line = '你好，2017！'
re_pattern = '.*?(\d+)'

re_pattern = '.*(\d{4})'

match_obj = re.match(re_pattern, line)
if match_obj:
    print(match_obj.group(1))