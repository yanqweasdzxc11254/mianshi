def Sum(nums, target):
    num_map = {} 
    for i, num in enumerate(nums):
        num_2 = target - num  # 计算补数
        if num_2 in num_map:
            return [num_map[num_2], i]  # 返回补数的索引 和 当前索引
        num_map[num] = i  # 将当前数字和索引加入哈希表


nums = [2, 7, 11, 15]
target = 13
result = Sum(nums, target)
print(result)  
