"""
简单选择排序：依次遍历未排序的列表，选出其中的最小值，插在对应的位置
第一次遍历[0:n]得到最小值，排在第一个位置，
第二次遍历[1:n]得到最小值，排在第二个位置，
。。。。

"""
def selectionSort(a_list):
    """
    选择排序
    :param a_list:
    :return:
    """
    a_len = len(a_list)
    for i in range(a_len):
        a_min = a_list[i]
        ind = i
        for j in range(i+1, a_len):
            if a_list[j] < a_min:
                a_min = a_list[j]
                ind = j
        tmp = a_list[i]
        a_list[i] = a_list[ind]
        a_list[ind] = tmp
        
    return a_list        


def bubbleSort(a_list):
    """
    冒泡排序：从小到大
    :param a_list:
    :return:
    """
    a_len = len(a_list)
    for i in range(a_len):
        for j in range(a_len-1-i):  # 已经冒泡排序号得就不需要再比对了
            if a_list[j+1] < a_list[j]:
                a_list[j+1], a_list[j] = a_list[j], a_list[j+1]

    return a_list


def insertSortSearch(a_list):
    """
    简单插入排序
    :param a_list:
    :return:
    """
    a_len = len(a_list)
    for i in range(1, a_len):
        # 从后往前遍历之前有序得列表
        tmp = a_list[i]
        flag = 0
        for j in range(i-1, -1, -1):
            if a_list[j] > tmp:
                a_list[j+1] = a_list[j]
            else:
                a_list[j+1] = tmp
                flag = 1
                break
        if not flag:
            a_list[0] = tmp

    return a_list


def shellSort(a_list):
    """
    希尔排序
    :param a_list:
    :return:
    """
    pass


def quickSort(a_list):
    """
    快速排序
    :param a_list:
    :return:
    """
    if not a_list:
        return []
    flag = a_list[0]
    return quickSort([i for i in a_list if i < flag]) + [i for i in a_list if i == flag] + quickSort([i for i in a_list if i > flag])


def mergeSortRecursive(a_list):
    """
    归并排序，主要采用递归 + 分治的策略
    :param a_list:
    :return:
    """
    a_len = len(a_list)
    if a_len > 1:
        resu_list = []
        left = mergeSortRecursive(a_list[:a_len//2])
        right = mergeSortRecursive(a_list[a_len//2:])
        left_len = len(left)
        right_len = len(right)
        i = 0
        j = 0
        while i < left_len and j < right_len:
            if left[i] < right[j]:
                resu_list.append(left[i])
                i += 1
            else:
                resu_list.append(right[j])
                j += 1
        if i < left_len:
            resu_list.extend(left[i:])
        if j < right_len:
            resu_list.extend(right[j:])
        return resu_list
    return a_list



if __name__ == "__main__":
    a_list = [3, 4, 1, 10, 8, 5, 9, 11, 18]
    # print(selectionSort(a_list))
    # print(bubbleSort(a_list))
    # print(insertSortSearch(a_list))
    # print(quickSort(a_list))
    print(mergeSortRecursive(a_list))








