#!/usr/bin/env python
# -*- coding:utf-8 -*-

def main():
    # 字符串
    s = "HelloWorld"
    # 转换成数组
    l = list(s)
    # 对数组排序，注意，该方法没有返回值
    l.sort()
    print('l = ', l)
    l = set(l)
    print('l = ', l)
    # 转换成数组
    s = "".join(l)
    print(s)
    # 结果如下：
    # !HWdellloor


# def _test(_list=[])

def Fib(n):
    '''
    假定序号为0或者1,返回1,序号为2时返回2
    '''
    before = 1
    after = 1
    for i in range(n):
        before, after = after, before + after
    return before


for i in range(10):
    print(Fib(i))

_a = "abc"
_b = "ABD"
_c = [1, 2, 3]
print(_a.join(_b))
# print(_a.join(_c))
s1 = "-"
s2 = ""
seq = ["r", "u", "n", "o", "o", "b"]  # 字符串序列
print(s1.join(seq))
print(s2.join(seq))


def partition(arr, low, high):
    i = (low - 1)  # 最小元素索引
    pivot = arr[high]

    for j in range(low, high):

        # 当前元素小于或等于 pivot
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)


# arr[] --> 排序数组
# low  --> 起始索引
# high  --> 结束索引

# 快速排序函数
def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


arr = [10, 7, 8, 9, 1, 5]
n = len(arr)
quickSort(arr, 0, n - 1)
print("排序后的数组:")
for i in range(n):
    print("%d" % arr[i]),


def extend_list(val, plist=[]):
    plist.append(val)
    return plist


list1 = extend_list(10)
list2 = extend_list(123, [])
list3 = extend_list('a')

print('list1 = ', list1)
print(list2)
print(list3)


def multipliners():
    return [lambda x: i * x for i in range(4)]


print([m(2) for m in multipliners()])

if __name__ == "__main__":
    main()
