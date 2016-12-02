a = list(range(1,101))
print(a)

# import urllib.request
 
# from multiprocessing.dummy import Pool as ThreadPool
 
# urls = ['http://www.baidu.com','http://www.sina.com','http://www.qq.com']
 
# pool = ThreadPool()
 
# results = pool.map(urllib.request.urlopen,urls)
# print(results)
# pool.close()
# pool.join()
 
# print('main ended')


# import time
# import datetime
# from functools import wraps


# def fn_timer(function):
#     @wraps(function)
#     def function_timer(*args, **kwargs):
#         t0 = datetime.datetime.now().microsecond
#         print(datetime.datetime.now())
#         result = function(*args, **kwargs)
#         t1 = datetime.datetime.now().microsecond
#         print("Total time running %s: %s seconds" %
#               (function.__name__, str(t1 - t0))
#               )
#         return result

#     return function_timer

# @fn_timer
# def twoSum(nums, target):
#     """
#     :type nums: List[int]
#     :type target: int
#     :rtype: List[int]
#     """
#     dict = {}

#     for i in range(len(nums)):
#         dict[nums[i]] = i


#     a = 0
#     for i in range(len(nums)):
#         a += 1
#         print(a)
#         diff = target-nums[i]

#         if diff in dict.keys() and dict[diff] != i:
#             return [i, dict[target-nums[i]]]

# @fn_timer
# def twoSum2(nums, target):
#     """
#     :type nums: List[int]
#     :type target: int
#     :rtype: List[int]
#     """
#     dict = {}

#     # for i in range(len(nums)):
#     #     dict[nums[i]] = i

#     a = 0
#     for i in range(len(nums)):
#         a += 1
#         print(i)
#         diff = target-nums[i]

#         if diff in dict.keys():
#             return [dict[target-nums[i]], i]
#         dict[nums[i]] = i


# def findTheDifference(s, t):
#     """
#     :type s: str
#     :type t: str
#     :rtype: str
#     """

#     dict = {}
#     for item in s:
#         if item in dict:
#             dict[item] += 1
#         else:
#             dict[item] = 1

#     dict2 = {}
#     for item in t:
#         if item in dict2:
#             dict2[item] += 1
#         else:
#             dict2[item] = 1

#     for item in t:
#         if (not item in dict) or dict[item]!=dict2[item]:
#             return item


# if __name__ == "__main__":
#     # print(twoSum([0,4,10,13,3,0], 0))
#     # print(twoSum2([0,4,10,13,3,0], 0))
#     print(findTheDifference("ae", "aea"))
