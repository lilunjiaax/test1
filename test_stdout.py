"""
样例输入
81 4
2 2

样例输出
94.73
3.41

"""
import sys


# while 1:
#     s = input()
#     if s != "":
#         m, n = [int(j) for j in s.split(' ')]
#         a_list = [m]
#         while len(a_list) != n:
#             m = m ** 0.5
#             a_list.append(m)
#         sum_list = round(sum(a_list), 2)
#         print(sum_list)
#     else:
#         break

"""
样例输入
100 120
300 380

样例输出
no
370 371
"""
def judge(num):
    a = num % 10
    b = num // 10 % 10
    c = num // 100
    if num == a**3 + b**3 + c**3:
        return True
    else:
        return False

while 1:
    s = input()
    if s != '':
        min, max = [int(j) for j in s.split(' ')]
        a_list = []
        while min <= max:
            if judge(min):
                a_list.append(min)
            min += 1
        if len(a_list) == 0:
            print('no')
        else:
            j = 0
            for i in a_list:
                if j == 0:
                    sys.stdout.write(str(i))
                    j += 1
                else:
                    sys.stdout.write(' ' + str(i))
            print('')
    else:
        break




