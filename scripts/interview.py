# 冒泡排序

# 快速排序

# 浅拷贝，深拷贝，切片 可变对象 不可变对象

# python实现栈结构

# python实现堆结构

# 生成器 跟 迭代器

# 谈谈GIL 锁

# 各个框架的区别

# 那些高并发的场景

# kafka 跟 es

# 重复消费

# 第三方库

# redis的过期策略

# 关于resf

# nginx 跟 uwsig

# 多线程是并发还是并行

# 面向对象语言实现一个生产者消费者模式的实例

# 列表[1, 4, 12, 45, 66, 99, 120, 44] 请用python 简单实现二分查找，查找99 出现的位置


a = list(range(2))


def test_(_list=[], add_list=[]):
    _list.extend(add_list)
    return _list


r1 = test_(a)
r2 = test_(a, r1)
r3 = test_(a, r2)
print(r1)
print(r2)
print(r3)


def test_yieled():
    print('A')
    yield 'B'
    print('C')
    yield 'D'
    print('E')
    yield 'F'


t = test_yieled()
print('-----')
print(next(t))
print('-----')
print(next(t))


def sum(n):
    if n == 1:
        return n
    else:
        return n + sum(n -1)

print(sum(10))
print(sum(100))
print(sum(998))

a_ = range(0, 20)[2:-2]
print(a_)