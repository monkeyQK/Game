# -*- coding: utf-8 -*-
# code by monkeyQK
# 炸金花小游戏
import random
from functools import reduce
import re

# 判断属于哪种牌型
# 返回值为 牌型代码+三个转换的数字
def card_type(d, L):
    num1 = int(L[0][1:])
    num2 = int(L[1][1:])
    num3 = int(L[2][1:])
    list1 = sorted([num1, num2, num3], reverse=True)
    num1_new = list1[0]
    num2_new = list1[1]
    num3_new = list1[2]

    # 三张牌都不相同的情况
    if num1 != num2 and num1 != num3 and num2 != num3:
        num1_type = L[0][0:1]
        num2_type = L[1][0:1]
        num3_type = L[2][0:1]
        if num1_type == num2_type and num2_type == num3_type:
            if ((num1-num2) == 1 and (num1-num3) == 2) or ((num2-num3) == 1 and (num2-num1) == 2) or ((num3-num2) == 1 and (num3-num1) == 2):
                return [5, num1_new, num2_new, num3_new]
            else:
                return [4, num1_new, num2_new, num3_new]
        if ((num1-num2) == 1 and (num1-num3) == 2) or ((num2-num3) == 1 and (num2-num1) == 2) or ((num3-num2) == 1 and (num3-num1) == 2):
            return [3, num1_new, num2_new, num3_new]
        else:
            return [1, num1_new, num2_new, num3_new]
    # 两张牌相同的情况
    if (num1 == num2 and num1 != num3) or (num1 == num3 and num1 != num2) or (num2 == num3 and num2 != num1):
        return [2, num1_new, num2_new, num3_new]
    # 三张牌相同的情况
    if (num1 == num2 and num2 == num3):
        return [6, num1_new, num2_new, num3_new]

# 根据牌型代码显示牌型名称
def poker_type(d, n, li):
    num1 = int(li[0])
    num2 = int(li[1])
    num3 = int(li[2])
    list1 = sorted([num1, num2, num3], reverse=True)
    card_info = list1
    result = ""
    if n == 1:
        result = "单牌"
    if n == 2:
        if num1 == num2:
            num_a = num1
            num_b = num3
        if num2 == num3:
            num_a = num2
            num_b = num1
        if num3 == num1:
            num_a = num3
            num_b = num2
        result = "一对%s" % find_bykey(d, num_a)
        card_info = [num_a, num_a, num_b]
    if n == 3:
        result = "顺子"
    if n == 4:
        result = "清一色"
    if n == 5:
        result = "顺金"
    if n == 6:
        result = "金花"
    return result, card_info

# 按牌大小排序 大的在前面

def poker_sorted(d):
    return sorted(d.items(), key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3]), reverse=True)


# 根据字典对照查找牌
def find_bykey(d, li):
    if isinstance(li, int):
        return d[li]
    li_new = []
    for i in li:
        li_new.append(d[i])
    return li_new


while True:
    # 定义牌的代码
    L = list(str(i)+str(j) for i in ["A", "B", "C", "D"] for j in range(2, 15))
    # 代码和牌 对应字典
    dict_poker = {"A14": "黑桃A", "A2": "黑桃2", "A3": "黑桃3", "A4": "黑桃4", "A5": "黑桃5", "A6": "黑桃6", "A7": "黑桃7",
                  "A8": "黑桃8", "A9": "黑桃9", "A10": "黑桃10", "A11": "黑桃J", "A12": "黑桃Q", "A13": "黑桃K",
                  "B14": "红桃A", "B2": "红桃2", "B3": "红桃3", "B4": "红桃4", "B5": "红桃5", "B6": "红桃6", "B7": "红桃7",
                  "B8": "红桃8", "B9": "红桃9", "B10": "红桃10", "B11": "红桃J", "B12": "红桃Q", "B13": "红桃K",
                  "C14": "梅花A", "C2": "梅花2", "C3": "梅花3", "C4": "梅花4", "C5": "梅花5", "C6": "梅花6", "C7": "梅花7",
                  "C8": "梅花8", "C9": "梅花9", "C10": "梅花10", "C11": "梅花J", "C12": "梅花Q", "C13": "梅花K",
                  "D14": "方块A", "D2": "方块2", "D3": "方块3", "D4": "方块4", "D5": "方块5", "D6": "方块6", "D7": "方块7",
                  "D8": "方块8", "D9": "方块9", "D10": "方块10", "D11": "方块J", "D12": "方块Q", "D13": "方块K",
                  1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
                  11: "J", 12: "Q", 13: "K", 14: "A"}

    print("*"*20+"炸金花开始"+"*"*20)
    players_num = int(input("有几个玩家参与？"))
    # 52张牌最多够17人玩
    if players_num > 17:
        print("牌不够发,重新开始！")
        continue
    print("*"*20+"开始**发牌"+"*"*20)
    players_poker = {}

    # 根据输入玩家数，随机发几份牌
    n = 0
    card_infos = []
    # 模拟每个玩家随机发一张，发3轮
    # 每随机发一张，从代码列表中删除这张
    while n < 3:
        for i in range(1, players_num+1):
            for j in random.sample(L, 1):
                card = (i, j)
                L.remove(j)
            card_infos.append(card)
        n += 1
    #发完牌的信息
    #print(card_infos)
    # 按玩家顺序1到N理好牌
    info_new = sorted(card_infos)
    #排好序的信息
    #print(info_new)
    # 把每一个玩家的牌放一个列表
    # 玩家序号作为key，玩家的三张牌作为value
    m = 1
    for i in range(0, len(info_new), 3):
        players_poker[m] = list(map(lambda x: x[1], info_new[i:i+3]))
        m += 1
    #按玩家把牌分开的信息
    #print(players_poker)
    tuple_player = []
    dict_player = {}
    # 显示玩家的牌
    for k, v in players_poker.items():
        print("玩家%s的牌:%s" % (k, find_bykey(dict_poker, v)))
        card_info = card_type(dict_poker, v)
        tuple_player.append([k, card_info])

    print("*"*20+"开始比大小"+"*"*20)
    #去掉花色的信息
    #print(tuple_player)
    for i in tuple_player:
        dict_player[i[0]] = i[1][:4]


    dict_playernew = {}
    for k, v in dict_player.items():
        b = poker_type(dict_poker, v[0], v[1:])[1]
        b.insert(0, v[0])
        dict_playernew[k] = b

    #转化为字典的信息
    #print(dict_playernew)
    list_playernew=poker_sorted(dict_playernew)
    #按大小排好的字典
    #print(list_playernew)
    sorts=1
    for k, v in list_playernew:
        a = poker_type(dict_poker, v[0], v[1:])[0]
        b = poker_type(dict_poker, v[0], v[1:])[1]
        b = find_bykey(dict_poker, b)
        b = reduce(lambda x, y: x+","+y, b)
        print("玩家%s的牌型是:\t%s\t%s\t第%s大" % (k, a, b, sorts))
        sorts += 1
    print("\n"*2)

    
