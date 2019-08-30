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
class Solution:
    def Permutation(self, ss):
        # write code here
        if not ss:
            return





















