"""
输入一个复杂链表（每个节点中有节点值，以及两个指针，一个指向下一个节点，另一个特殊指针指向任意一个节点），
返回结果为复制后复杂链表的head。（注意，输出结果中请不要返回参数中的节点引用，否则判题程序会直接返回空）
"""
# -*- coding:utf-8 -*-
# class RandomListNode:
#     def __init__(self, x):
#         self.label = x
#         self.next = None
#         self.random = None
# class Solution:
#     # 返回 RandomListNode
#     def Clone(self, pHead):
#         # write code here
#         p = pHead
#         # 复制
#         while p:
#             temp = p.next
#             des = RandomListNode(p.label)
#             p.next = des
#             des.next = temp
#             p = temp
#
#         # 确定随机指针
#         p = pHead
#         while p:
#             des = p.next
#             if p.random:
#                 des.random = p.random.next
#             p = des.next
#         # 进行分离操作
#         head = pHead.next
#         p = head
#         while p.next:
#             temp = p.next.next
#             p.next = temp
#             p = temp
#
#         return head

#
# class Solution:
#     # 返回 RandomListNode
#     def Clone(self, pHead):
#         # write code here
#         head = pHead
#         p_head = None
#         new_head = None
#
#         random_dic = {}
#         old_new_dic = {}
#
#         while head:
#             node = RandomListNode(head.label)
#             node.random = head.random
#             old_new_dic[id(head)] = id(node)
#             random_dic[id(node)] = node
#             head = head.next
#
#             if new_head:
#                 new_head.next = node
#                 new_head = new_head.next
#             else:
#                 new_head = node
#                 p_head = node
#
#         new_head = p_head
#         while new_head:
#             if new_head.random != None:
#                 # 在 id(1) : id(2) 和 id(2) : node 之间建立了对照关系字典
#                 new_head.random = random_dic[old_new_dic[id(new_head.random)]]
#             new_head = new_head.next
#         return p_head
#
# a = RandomListNode(1)
# b = RandomListNode(2)
# c = RandomListNode(3)
#
# a.next = b
# b.next = c
# a.random = c
#
# so = Solution()
# so.Clone(a)


"""
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的双向链表。
要求不能创建任何新的结点，只能调整树中结点指针的指向。
"""

# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
#
# class Solution:
#     def __init__(self):
#         self.stack = []
#         self.middle = []
#     def push(self, item):
#         self.stack.append(item)
#     def pop(self):
#         return self.stack.pop()
#
#     def Convert(self, pRootOfTree):
#         # write code here
#         if not pRootOfTree:
#             return None
#
#         p = pRootOfTree
#         while p or self.stack:
#             while p:
#                 self.push(p)
#                 p = p.left
#             if self.stack:
#                 p = self.pop()
#                 self.middle.append(p)
#                 p = p.right
#         for i in range(len(self.middle)-1):
#             self.middle[i].right = self.middle[i+1]
#             self.middle[i+1].left = self.middle[i]
#         return self.middle[0]
#
# root = TreeNode(5)
# four = TreeNode(4)
# three = TreeNode(3)
# seven = TreeNode(7)
# root.left = four
# root.right = seven
#
# four.left = three
#
# so = Solution()
# so.Convert(root)

"""
题目描述
输入一个字符串,按字典序打印出该字符串中字符的所有排列。
例如输入字符串abc,则打印出由字符a,b,c所能排列出来的所有字符串abc,acb,bac,bca,cab和cba。
输入描述:
输入一个字符串,长度不超过9(可能有字符重复),字符只包括大小写字母。
"""
"""
这一类问题一般可以概括为树形问题：

"""
# -*- coding:utf-8 -*-
# class Solution:
#     def Permutation(self, ss):
#         # write code here
#         if not ss:
#             return []
#         res = []
#         self.digui(ss, res, '')
#         return sorted(list(set(res)))
#
#     def digui(self, ss, res, path):
#         if not ss:
#             res.append(path)
#         else:
#             for i in range(len(ss)):
#                 self.digui(ss[:i]+ss[i+1:], res, path+ss[i])
#
#
#
# so = Solution()
# so.Permutation('abc')


"""
数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。
例如输入一个长度为9的数组{1,2,3,2,2,2,5,4,2}。由于数字2在数组中出现了5次，
超过数组长度的一半，因此输出2。如果不存在则输出0。
"""

# -*- coding:utf-8 -*-
# class Solution:
#     def MoreThanHalfNum_Solution(self, numbers):
#         # write code here
#         '''
#         进行排序
#         :param numbers:
#         :return:
#         '''
#         numbers.sort()
#         count = len(numbers)
#         des = numbers[count // 2]
#         cou = numbers.count(des)
#         if cou > count//2:
#
#             return numbers[count // 2]
#         else:
#             return 0
#
# so = Solution()
# print(so.MoreThanHalfNum_Solution([1, 2, 3, 2, 2, 2, 5, 4, 2]))

"""
输入n个整数，找出其中最小的K个数。例如输入4,5,1,6,2,7,3,8这8个数字，则最小的4个数字是1,2,3,4,。
"""
# -*- coding:utf-8 -*-
# class Solution:
#     def GetLeastNumbers_Solution(self, tinput, k):
#         # write code here
#         if k>len(tinput):
#             return []
#         tinput.sort()
#         return tinput[0:k]


"""
HZ偶尔会拿些专业问题来忽悠那些非计算机专业的同学。
今天测试组开完会后,
他又发话了:在古老的一维模式识别中,常常需要计算连续子向量的最大和,
当向量全为正数的时候,问题很好解决。
但是,如果向量中包含负数,是否应该包含某个负数,并期望旁边的正数会弥补它呢？
例如:{6,-3,-2,7,-15,1,2,2},连续子向量的最大和为8(从第0个开始,到第3个为止)。
给一个数组，返回它的最大连续子序列的和，你会不会被他忽悠住？(子向量的长度至少是1)
"""

# -*- coding:utf-8 -*-
# class Solution:
#     def FindGreatestSumOfSubArray(self, array):
#         # write code here
#         a_count = len(array)
#         a_dict = {}
#         b_dict = {}
#         i = 0
#         while i< a_count:
#             if array[i] > 0:
#                 # 求正串的和
#                 sum1, id1 = self.get_sum(array, i, 1)
#                 a_dict[id1-1] = sum1
#                 i = id1
#                 continue
#             if array[i] < 0:
#                 sum1, id1 = self.get_sum(array, i, 0)
#                 a_dict[id1-1] = sum1
#                 i = id1
#                 continue
#             if array[i] == 0:
#                 i = i+1
#                 continue
#
#
#     def get_sum(self, array, i, flag):
#         if flag == 1:
#             # 求正串的和
#             res = []
#             for j in range(i, len(array)):
#                 if array[j] < 0:
#                     break
#                 res.append(array[j])
#             return sum(res), j
#         elif flag == 0:
#             # 求负串的和
#             res = []
#             for j in range(i, len(array)):
#                 if array[j] > 0:
#                     break
#                 res.append(array[j])
#             return sum(res), j

# class Solution:
#     def FindGreatestSumOfSubArray(self, array):
#         maxsum, maxhere = array[0], array[0]
#         for i in array[1:]:
#             if maxhere <= 0:
#                 maxhere = i
#             else:
#                 maxhere += i
#             if maxhere > maxsum:
#                 maxsum = maxhere
#         return maxsum
#
#
# so = Solution()
# so.FindGreatestSumOfSubArray([6, -3, -2, 7, -15, 1, 2, 2])


"""
求出1~13的整数中1出现的次数,并算出100~1300的整数中1出现的次数？
为此他特别数了一下1~13中包含1的数字有1、10、11、12、13因此共出现6次,但是对于后面问题他就没辙了。
ACMer希望你们帮帮他,并把问题更加普遍化,可以很快的求出任意非负整数区间中1出现的次数（从1 到 n 中1出现的次数）。
"""


# -*- coding:utf-8 -*-
# class Solution:
#     def NumberOf1Between1AndN_Solution(self, n):
#         # write code here
#         a_str = ''
#         for i in range(1, n + 1):
#             a_str += str(i)
#         return a_str.count('1')

"""
输入一个正整数数组，把数组里所有数字拼接起来排成一个数，
打印能拼接出的所有数字中最小的一个。例如输入数组{3，32，321}，则打印出这三个数字能排成的最小数字为321323。
"""

# -*- coding:utf-8 -*-
# class Solution:
#     def PrintMinNumber(self, numbers):
#         if not numbers:
#             return ''
#         # write code here
#         numbers = [str(i) for i in numbers]
#         numbers = self.Permutation(numbers)
#         numbers = [int(i) for i in numbers]
#         return min(numbers)
#
#     def Permutation(self, ss):
#         # write code here
#         if not ss:
#             return []
#         res = []
#         self.digui(ss, res, '')
#         return sorted(list(set(res)))
#
#     def digui(self, ss, res, path):
#         if not ss:
#             res.append(path)
#         else:
#             for i in range(len(ss)):
#                 self.digui(ss[:i]+ss[i+1:], res, path+ss[i])

"""
把只包含质因子2、3和5的数称作丑数（Ugly Number）。
例如6、8都是丑数，但14不是，
因为它包含质因子7。 习惯上我们把1当做是第一个丑数。求按从小到大的顺序的第N个丑数。
"""
# -*- coding:utf-8 -*-
class Solution:
    def GetUglyNumber_Solution(self, index):
        # write code here















