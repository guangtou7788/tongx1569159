#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import random
import logging
from datetime import datetime
import requests

BARK_KEY = "WnpcNyZjd93bSubYD7Gx2N"
BARK_URL = f"https://api.day.app/{BARK_KEY}/"

def bark_push(title: str, body: str = ""):
    """推送结果到 Bark"""
    url = BARK_URL + requests.utils.quote(title)
    if body:
        url += "?body=" + requests.utils.quote(body)
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        logging.warning(f"Bark 推送失败: {e}")

# 初始化基础控制台日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# --------------------------------------------------
# 1. 产品配置表：按顺序跑
PRODUCTS = [
    {"name": "悦享涂氟", "code": "1000804"},

]

# --------------------------------------------------
# 2. 请求头模板
HEADERS_TPL = {
    "Host": "ebkapi.17u.cn",
    "Accept": "application/json, text/plain, */*",
    "type": "M",
    "Content-Type": "application/json",
    "Origin": "https://hy.txhmo.com",
    "Referer": "https://hy.txhmo.com/",
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
    "token": "f2436cdd-e3ad-47ef-80ab-e007bdb5614a",  
}

# --------------------------------------------------
# 3. 固定城市数据
CITY_DATA_RAW = {
    "code": "200", "message": "操作成功",
    "data": {
        "A": [{"id": 36, "name": "安庆", "prefixLetter": "A"}, {"id": 112, "name": "安顺", "prefixLetter": "A"},
              {"id": 150, "name": "安阳", "prefixLetter": "A"}, {"id": 245, "name": "鞍山", "prefixLetter": "A"}],
        "B": [{"id": 37, "name": "蚌埠", "prefixLetter": "B"}, {"id": 52, "name": "亳州", "prefixLetter": "B"},
              {"id": 53, "name": "北京", "prefixLetter": "B"}, {"id": 63, "name": "白银", "prefixLetter": "B"},
              {"id": 98, "name": "百色", "prefixLetter": "B"}, {"id": 99, "name": "北海", "prefixLetter": "B"},
              {"id": 113, "name": "毕节", "prefixLetter": "B"},
              {"id": 139, "name": "保定", "prefixLetter": "B"}, {"id": 212, "name": "白城", "prefixLetter": "B"},
              {"id": 213, "name": "白山", "prefixLetter": "B"}, {"id": 246, "name": "本溪", "prefixLetter": "B"},
              {"id": 260, "name": "巴彦淖尔市", "prefixLetter": "B"}, {"id": 261, "name": "包头", "prefixLetter": "B"},
              {"id": 283, "name": "滨州", "prefixLetter": "B"}, {"id": 312, "name": "宝鸡", "prefixLetter": "B"},
              {"id": 323, "name": "巴中", "prefixLetter": "B"},
              {"id": 367, "name": "保山", "prefixLetter": "B"}, {"id": 44683, "name": "北屯", "prefixLetter": "B"},
              {"id": 44686, "name": "大理白族自治州", "prefixLetter": "B"}],
        "C": [{"id": 38, "name": "巢湖", "prefixLetter": "C"}, {"id": 39, "name": "池州", "prefixLetter": "C"},
              {"id": 40, "name": "滁州", "prefixLetter": "C"}, {"id": 77, "name": "潮州", "prefixLetter": "C"},
              {"id": 100, "name": "崇左", "prefixLetter": "C"},
              {"id": 124, "name": "澄迈县", "prefixLetter": "C"}, {"id": 140, "name": "沧州", "prefixLetter": "C"},
              {"id": 141, "name": "承德", "prefixLetter": "C"}, {"id": 198, "name": "常德", "prefixLetter": "C"},
              {"id": 199, "name": "长沙", "prefixLetter": "C"}, {"id": 200, "name": "郴州", "prefixLetter": "C"},
              {"id": 214, "name": "长春", "prefixLetter": "C"}, {"id": 221, "name": "常州", "prefixLetter": "C"},
              {"id": 247, "name": "朝阳", "prefixLetter": "C"}, {"id": 262, "name": "赤峰", "prefixLetter": "C"},
              {"id": 300, "name": "长治", "prefixLetter": "C"}, {"id": 324, "name": "成都", "prefixLetter": "C"},
              {"id": 345, "name": "昌都", "prefixLetter": "C"},
              {"id": 355, "name": "昌吉回族自治州", "prefixLetter": "C"},
              {"id": 368, "name": "楚雄彝族自治州", "prefixLetter": "C"},
              {"id": 394, "name": "重庆", "prefixLetter": "C"}, {"id": 4569, "name": "长白山", "prefixLetter": "C"}],
        "D": [{"id": 64, "name": "定西", "prefixLetter": "D"}, {"id": 78, "name": "东莞", "prefixLetter": "D"},
              {"id": 125, "name": "定安县", "prefixLetter": "D"}, {"id": 126, "name": "东方", "prefixLetter": "D"},
              {"id": 138, "name": "儋州", "prefixLetter": "D"}, {"id": 168, "name": "大庆", "prefixLetter": "D"},
              {"id": 169, "name": "大兴安岭", "prefixLetter": "D"}, {"id": 248, "name": "大连", "prefixLetter": "D"},
              {"id": 249, "name": "丹东", "prefixLetter": "D"}, {"id": 284, "name": "德州", "prefixLetter": "D"},
              {"id": 285, "name": "东营", "prefixLetter": "D"}, {"id": 301, "name": "大同", "prefixLetter": "D"},
              {"id": 325, "name": "达州", "prefixLetter": "D"}, {"id": 326, "name": "德阳", "prefixLetter": "D"},
              {"id": 369, "name": "大理", "prefixLetter": "D"}],
        "E": [{"id": 181, "name": "鄂州", "prefixLetter": "E"},
              {"id": 263, "name": "鄂尔多斯", "prefixLetter": "E"}],
        "F": [{"id": 41, "name": "阜阳", "prefixLetter": "F"}, {"id": 54, "name": "福州", "prefixLetter": "F"},
              {"id": 79, "name": "佛山", "prefixLetter": "F"}, {"id": 101, "name": "防城港", "prefixLetter": "F"},
              {"id": 234, "name": "抚州", "prefixLetter": "F"}, {"id": 250, "name": "抚顺", "prefixLetter": "F"},
              {"id": 251, "name": "阜新", "prefixLetter": "F"}, {"id": 44190, "name": "抚远市", "prefixLetter": "F"}],
        "G": [{"id": 80, "name": "广州", "prefixLetter": "G"}, {"id": 102, "name": "桂林", "prefixLetter": "G"},
              {"id": 103, "name": "贵港", "prefixLetter": "G"}, {"id": 114, "name": "贵阳", "prefixLetter": "G"},
              {"id": 235, "name": "赣州", "prefixLetter": "G"}, {"id": 271, "name": "固原", "prefixLetter": "G"},
              {"id": 328, "name": "广安", "prefixLetter": "G"}, {"id": 329, "name": "广元", "prefixLetter": "G"},
              {"id": 397, "name": "高雄", "prefixLetter": "G"}],
        "H": [{"id": 42, "name": "合肥", "prefixLetter": "H"}, {"id": 43, "name": "淮北", "prefixLetter": "H"},
              {"id": 44, "name": "淮南", "prefixLetter": "H"}, {"id": 45, "name": "黄山", "prefixLetter": "H"},
              {"id": 81, "name": "河源", "prefixLetter": "H"}, {"id": 82, "name": "惠州", "prefixLetter": "H"},
              {"id": 104, "name": "河池", "prefixLetter": "H"}, {"id": 105, "name": "贺州", "prefixLetter": "H"},
              {"id": 127, "name": "海口", "prefixLetter": "H"}, {"id": 142, "name": "邯郸", "prefixLetter": "H"},
              {"id": 143, "name": "衡水", "prefixLetter": "H"}, {"id": 151, "name": "鹤壁", "prefixLetter": "H"},
              {"id": 170, "name": "哈尔滨", "prefixLetter": "H"}, {"id": 171, "name": "鹤岗", "prefixLetter": "H"},
              {"id": 172, "name": "黑河", "prefixLetter": "H"}, {"id": 183, "name": "黄冈", "prefixLetter": "H"},
              {"id": 184, "name": "黄石", "prefixLetter": "H"}, {"id": 201, "name": "衡阳", "prefixLetter": "H"},
              {"id": 202, "name": "怀化", "prefixLetter": "H"}, {"id": 222, "name": "淮安", "prefixLetter": "H"},
              {"id": 252, "name": "葫芦岛", "prefixLetter": "H"}, {"id": 264, "name": "呼和浩特", "prefixLetter": "H"},
              {"id": 265, "name": "呼伦贝尔", "prefixLetter": "H"},
              {"id": 286, "name": "菏泽", "prefixLetter": "H"}, {"id": 313, "name": "汉中", "prefixLetter": "H"},
              {"id": 356, "name": "哈密", "prefixLetter": "H"}, {"id": 357, "name": "和田", "prefixLetter": "H"},
              {"id": 372, "name": "红河哈尼族彝族自治州", "prefixLetter": "H"},
              {"id": 383, "name": "杭州", "prefixLetter": "H"}, {"id": 384, "name": "湖州", "prefixLetter": "H"},
              {"id": 398, "name": "花莲", "prefixLetter": "H"}],
        "J": [{"id": 66, "name": "嘉峪关", "prefixLetter": "J"}, {"id": 67, "name": "金昌", "prefixLetter": "J"},
              {"id": 68, "name": "酒泉", "prefixLetter": "J"}, {"id": 83, "name": "江门", "prefixLetter": "J"},
              {"id": 84, "name": "揭阳", "prefixLetter": "J"}, {"id": 152, "name": "济源", "prefixLetter": "J"},
              {"id": 153, "name": "焦作", "prefixLetter": "J"}, {"id": 173, "name": "鸡西", "prefixLetter": "J"},
              {"id": 174, "name": "佳木斯", "prefixLetter": "J"}, {"id": 185, "name": "荆门", "prefixLetter": "J"},
              {"id": 186, "name": "荆州", "prefixLetter": "J"}, {"id": 215, "name": "吉林", "prefixLetter": "J"},
              {"id": 236, "name": "吉安", "prefixLetter": "J"}, {"id": 237, "name": "景德镇", "prefixLetter": "J"},
              {"id": 238, "name": "九江", "prefixLetter": "J"}, {"id": 253, "name": "锦州", "prefixLetter": "J"},
              {"id": 287, "name": "济南", "prefixLetter": "J"}, {"id": 288, "name": "济宁", "prefixLetter": "J"},
              {"id": 302, "name": "晋城", "prefixLetter": "J"}, {"id": 303, "name": "晋中", "prefixLetter": "J"},
              {"id": 385, "name": "嘉兴", "prefixLetter": "J"}, {"id": 386, "name": "金华", "prefixLetter": "J"},
              {"id": 399, "name": "基隆", "prefixLetter": "J"}, {"id": 400, "name": "嘉义", "prefixLetter": "J"},
              {"id": 5127, "name": "金门", "prefixLetter": "J"}],
        "K": [{"id": 154, "name": "开封", "prefixLetter": "K"}, {"id": 373, "name": "昆明", "prefixLetter": "K"}],
        "L": [{"id": 46, "name": "六安", "prefixLetter": "L"}, {"id": 55, "name": "龙岩", "prefixLetter": "L"},
              {"id": 69, "name": "兰州", "prefixLetter": "L"},
              {"id": 71, "name": "陇南", "prefixLetter": "L"}, {"id": 106, "name": "来宾", "prefixLetter": "L"},
              {"id": 107, "name": "柳州", "prefixLetter": "L"}, {"id": 115, "name": "六盘水", "prefixLetter": "L"},
              {"id": 128, "name": "乐东黎族自治县", "prefixLetter": "L"},
              {"id": 129, "name": "临高县", "prefixLetter": "L"},
              {"id": 130, "name": "陵水黎族自治县", "prefixLetter": "L"},
              {"id": 144, "name": "廊坊", "prefixLetter": "L"}, {"id": 155, "name": "洛阳", "prefixLetter": "L"},
              {"id": 166, "name": "漯河", "prefixLetter": "L"}, {"id": 203, "name": "娄底", "prefixLetter": "L"},
              {"id": 216, "name": "辽源", "prefixLetter": "L"}, {"id": 223, "name": "连云港", "prefixLetter": "L"},
              {"id": 254, "name": "辽阳", "prefixLetter": "L"}, {"id": 289, "name": "莱芜", "prefixLetter": "L"},
              {"id": 290, "name": "聊城", "prefixLetter": "L"}, {"id": 291, "name": "临沂", "prefixLetter": "L"},
              {"id": 304, "name": "临汾", "prefixLetter": "L"}, {"id": 305, "name": "吕梁", "prefixLetter": "L"},
              {"id": 342, "name": "泸州", "prefixLetter": "L"}, {"id": 346, "name": "拉萨", "prefixLetter": "L"},
              {"id": 347, "name": "林芝", "prefixLetter": "L"}, {"id": 374, "name": "丽江", "prefixLetter": "L"},
              {"id": 375, "name": "临沧", "prefixLetter": "L"}, {"id": 387, "name": "丽水", "prefixLetter": "L"}],
        "M": [{"id": 47, "name": "马鞍山", "prefixLetter": "M"}, {"id": 85, "name": "茂名", "prefixLetter": "M"},
              {"id": 86, "name": "梅州", "prefixLetter": "M"}, {"id": 175, "name": "牡丹江", "prefixLetter": "M"},
              {"id": 332, "name": "眉山", "prefixLetter": "M"}, {"id": 333, "name": "绵阳", "prefixLetter": "M"},
              {"id": 5117, "name": "苗栗", "prefixLetter": "M"}],
        "N": [{"id": 56, "name": "南平", "prefixLetter": "N"}, {"id": 57, "name": "宁德", "prefixLetter": "N"},
              {"id": 108, "name": "南宁", "prefixLetter": "N"}, {"id": 156, "name": "南阳", "prefixLetter": "N"},
              {"id": 224, "name": "南京", "prefixLetter": "N"}, {"id": 225, "name": "南通", "prefixLetter": "N"},
              {"id": 239, "name": "南昌", "prefixLetter": "N"}, {"id": 334, "name": "南充", "prefixLetter": "N"},
              {"id": 335, "name": "内江", "prefixLetter": "N"},{"id": 388, "name": "宁波", "prefixLetter": "N"},
              {"id": 5119, "name": "南投", "prefixLetter": "N"}],
        "P": [{"id": 58, "name": "莆田", "prefixLetter": "P"}, {"id": 72, "name": "平凉", "prefixLetter": "P"},
              {"id": 157, "name": "平顶山", "prefixLetter": "P"}, {"id": 167, "name": "濮阳", "prefixLetter": "P"},
              {"id": 240, "name": "萍乡", "prefixLetter": "P"}, {"id": 255, "name": "盘锦", "prefixLetter": "P"},
              {"id": 336, "name": "攀枝花", "prefixLetter": "P"}, {"id": 378, "name": "普洱", "prefixLetter": "P"},
              {"id": 5121, "name": "屏东", "prefixLetter": "P"}, {"id": 5130, "name": "澎湖", "prefixLetter": "P"}],
        "Q": [{"id": 59, "name": "泉州", "prefixLetter": "Q"}, {"id": 73, "name": "庆阳", "prefixLetter": "Q"},
              {"id": 87, "name": "清远", "prefixLetter": "Q"}, {"id": 109, "name": "钦州", "prefixLetter": "Q"},
              {"id": 116, "name": "黔东南苗族侗族自治州", "prefixLetter": "Q"},
              {"id": 145, "name": "秦皇岛", "prefixLetter": "Q"}, {"id": 176, "name": "七台河", "prefixLetter": "Q"},
              {"id": 177, "name": "齐齐哈尔", "prefixLetter": "Q"}, {"id": 187, "name": "潜江", "prefixLetter": "Q"},
              {"id": 292, "name": "青岛", "prefixLetter": "Q"}, {"id": 377, "name": "曲靖", "prefixLetter": "Q"},
              {"id": 393, "name": "衢州", "prefixLetter": "Q"}],
        "R": [{"id": 293, "name": "日照", "prefixLetter": "R"}, {"id": 349, "name": "日喀则", "prefixLetter": "R"}],
        "S": [{"id": 48, "name": "宿州", "prefixLetter": "S"}, {"id": 60, "name": "三明", "prefixLetter": "S"},
              {"id": 88, "name": "汕头", "prefixLetter": "S"}, {"id": 89, "name": "汕尾", "prefixLetter": "S"},
              {"id": 90, "name": "韶关", "prefixLetter": "S"}, {"id": 91, "name": "深圳", "prefixLetter": "S"},
              {"id": 133, "name": "三亚", "prefixLetter": "S"}, {"id": 146, "name": "石家庄", "prefixLetter": "S"},
              {"id": 158, "name": "三门峡", "prefixLetter": "S"}, {"id": 159, "name": "商丘", "prefixLetter": "S"},
              {"id": 178, "name": "双鸭山", "prefixLetter": "S"}, {"id": 179, "name": "绥化", "prefixLetter": "S"},
              {"id": 188, "name": "神农架林区", "prefixLetter": "S"}, {"id": 189, "name": "十堰", "prefixLetter": "S"},
              {"id": 190, "name": "随州", "prefixLetter": "S"}, {"id": 204, "name": "邵阳", "prefixLetter": "S"},
              {"id": 217, "name": "四平", "prefixLetter": "S"}, {"id": 218, "name": "松原", "prefixLetter": "S"},
              {"id": 226, "name": "苏州", "prefixLetter": "S"}, {"id": 227, "name": "宿迁", "prefixLetter": "S"},
              {"id": 241, "name": "上饶", "prefixLetter": "S"}, {"id": 256, "name": "沈阳", "prefixLetter": "S"},
              {"id": 272, "name": "石嘴山", "prefixLetter": "S"}, {"id": 306, "name": "朔州", "prefixLetter": "S"},
              {"id": 314, "name": "商洛", "prefixLetter": "S"}, {"id": 321, "name": "上海", "prefixLetter": "S"},
              {"id": 337, "name": "遂宁", "prefixLetter": "S"}, {"id": 350, "name": "山南", "prefixLetter": "S"},
              {"id": 361, "name": "石河子", "prefixLetter": "S"}, {"id": 389, "name": "绍兴", "prefixLetter": "S"},
              {"id": 6321, "name": "三沙市", "prefixLetter": "S"}, {"id": 44684, "name": "双河", "prefixLetter": "S"}],
        "T": [{"id": 49, "name": "铜陵", "prefixLetter": "T"}, {"id": 74, "name": "天水", "prefixLetter": "T"},
              {"id": 119, "name": "铜仁", "prefixLetter": "T"}, {"id": 134, "name": "屯昌县", "prefixLetter": "T"},
              {"id": 147, "name": "唐山", "prefixLetter": "T"}, {"id": 191, "name": "天门", "prefixLetter": "T"},
              {"id": 219, "name": "通化", "prefixLetter": "T"}, {"id": 228, "name": "泰州", "prefixLetter": "T"},
              {"id": 257, "name": "铁岭", "prefixLetter": "T"}, {"id": 266, "name": "通辽", "prefixLetter": "T"},
              {"id": 294, "name": "泰安", "prefixLetter": "T"}, {"id": 307, "name": "太原", "prefixLetter": "T"},
              {"id": 315, "name": "铜川", "prefixLetter": "T"}, {"id": 343, "name": "天津", "prefixLetter": "T"}],
        "W": [{"id": 50, "name": "芜湖", "prefixLetter": "W"}, {"id": 75, "name": "武威", "prefixLetter": "W"},
              {"id": 110, "name": "梧州", "prefixLetter": "W"}, {"id": 135, "name": "万宁", "prefixLetter": "W"},
              {"id": 136, "name": "文昌", "prefixLetter": "W"}, {"id": 137, "name": "五指山", "prefixLetter": "W"},
              {"id": 192, "name": "武汉", "prefixLetter": "W"}, {"id": 229, "name": "无锡", "prefixLetter": "W"},
              {"id": 296, "name": "潍坊", "prefixLetter": "W"}, {"id": 316, "name": "渭南", "prefixLetter": "W"},
              {"id": 364, "name": "乌鲁木齐", "prefixLetter": "W"}, {"id": 365, "name": "五家渠", "prefixLetter": "W"},
              {"id": 379, "name": "文山壮族苗族自治州", "prefixLetter": "W"},
              {"id": 391, "name": "温州", "prefixLetter": "W"}, {"id": 3143, "name": "乌苏里江", "prefixLetter": "W"}],
        "X": [{"id": 51, "name": "宣城", "prefixLetter": "X"}, {"id": 61, "name": "厦门", "prefixLetter": "X"},
              {"id": 148, "name": "邢台", "prefixLetter": "X"}, {"id": 160, "name": "新乡", "prefixLetter": "X"},
              {"id": 161, "name": "信阳", "prefixLetter": "X"}, {"id": 162, "name": "许昌", "prefixLetter": "X"},
              {"id": 193, "name": "仙桃", "prefixLetter": "X"}, {"id": 194, "name": "咸宁", "prefixLetter": "X"},
              {"id": 195, "name": "襄阳", "prefixLetter": "X"}, {"id": 196, "name": "孝感", "prefixLetter": "X"},
              {"id": 205, "name": "湘潭", "prefixLetter": "X"},
              {"id": 206, "name": "湘西土家族苗族自治州", "prefixLetter": "X"},
              {"id": 230, "name": "徐州", "prefixLetter": "X"}, {"id": 242, "name": "新余", "prefixLetter": "X"},{"id": 281, "name": "西宁", "prefixLetter": "X"},
              {"id": 308, "name": "忻州", "prefixLetter": "X"}, {"id": 317, "name": "西安", "prefixLetter": "X"},
              {"id": 318, "name": "咸阳", "prefixLetter": "X"}],
        "Y": [{"id": 92, "name": "阳江", "prefixLetter": "Y"}, {"id": 93, "name": "云浮", "prefixLetter": "Y"},
              {"id": 111, "name": "玉林", "prefixLetter": "Y"}, {"id": 180, "name": "伊春", "prefixLetter": "Y"},
              {"id": 197, "name": "宜昌", "prefixLetter": "Y"}, {"id": 207, "name": "益阳", "prefixLetter": "Y"},
              {"id": 208, "name": "永州", "prefixLetter": "Y"}, {"id": 209, "name": "岳阳", "prefixLetter": "Y"},
              {"id": 220, "name": "延边朝鲜族自治州", "prefixLetter": "Y"},
              {"id": 231, "name": "盐城", "prefixLetter": "Y"}, {"id": 232, "name": "扬州", "prefixLetter": "Y"},
              {"id": 243, "name": "宜春", "prefixLetter": "Y"}, {"id": 244, "name": "鹰潭", "prefixLetter": "Y"},
              {"id": 258, "name": "营口", "prefixLetter": "Y"}, {"id": 274, "name": "银川", "prefixLetter": "Y"},
              {"id": 282, "name": "玉树藏族自治州", "prefixLetter": "Y"},
              {"id": 297, "name": "烟台", "prefixLetter": "Y"}, {"id": 309, "name": "阳泉", "prefixLetter": "Y"},
              {"id": 310, "name": "运城", "prefixLetter": "Y"}, {"id": 319, "name": "延安", "prefixLetter": "Y"},
              {"id": 320, "name": "榆林", "prefixLetter": "Y"}, {"id": 338, "name": "雅安", "prefixLetter": "Y"},
              {"id": 339, "name": "宜宾", "prefixLetter": "Y"},
              {"id": 381, "name": "玉溪", "prefixLetter": "Y"}, {"id": 5115, "name": "宜兰", "prefixLetter": "Y"},
              {"id": 5120, "name": "云林", "prefixLetter": "Y"}],
        "Z": [{"id": 62, "name": "漳州", "prefixLetter": "Z"}, {"id": 76, "name": "张掖", "prefixLetter": "Z"},
              {"id": 94, "name": "湛江", "prefixLetter": "Z"}, {"id": 95, "name": "肇庆", "prefixLetter": "Z"},
              {"id": 96, "name": "中山", "prefixLetter": "Z"}, {"id": 97, "name": "珠海", "prefixLetter": "Z"},
              {"id": 120, "name": "遵义", "prefixLetter": "Z"}, {"id": 149, "name": "张家口", "prefixLetter": "Z"},
              {"id": 163, "name": "郑州", "prefixLetter": "Z"}, {"id": 164, "name": "周口", "prefixLetter": "Z"},
              {"id": 165, "name": "驻马店", "prefixLetter": "Z"}, {"id": 210, "name": "张家界", "prefixLetter": "Z"},
              {"id": 211, "name": "株洲", "prefixLetter": "Z"}, {"id": 233, "name": "镇江", "prefixLetter": "Z"},
              {"id": 298, "name": "枣庄", "prefixLetter": "Z"}, {"id": 299, "name": "淄博", "prefixLetter": "Z"},
              {"id": 340, "name": "资阳", "prefixLetter": "Z"}, {"id": 341, "name": "自贡", "prefixLetter": "Z"},
              {"id": 382, "name": "昭通", "prefixLetter": "Z"}, {"id": 392, "name": "舟山", "prefixLetter": "Z"},
              {"id": 3105, "name": "中卫", "prefixLetter": "Z"}, {"id": 5118, "name": "彰化", "prefixLetter": "Z"}]
    },
    "success": True
}

# ---------- 工具 ----------
def now_str():
    return datetime.now().strftime("%m%d")

def load_cities():
    """把你给的城市 JSON 摊平成 list"""
    if CITY_DATA_RAW.get("code") != "200":
        raise RuntimeError("城市数据格式错误")
    cities = []
    for group in CITY_DATA_RAW["data"].values():
        cities.extend(group)
    return cities

def post_office_list(city_id, product_code):
    url = "https://ebkapi.17u.cn/hospital/supplier/office/list"
    payload = {
        "cityId": city_id,
        "keywords": "",
        "longitude": "",
        "latitude": "",
        "productCode": product_code,
        "sortType": "1",
    }
    for attempt in range(1, 4):
        try:
            time.sleep(random.uniform(0.5, 1.0))
            resp = requests.post(url, headers=HEADERS_TPL, json=payload, timeout=12)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") == "200":
                return data.get("data", [])
            logging.warning(f"API 返回异常状态码/信息: {data.get('message')}  attempt={attempt}")
        except Exception as e:
            logging.warning(f"请求失败: {e}  attempt={attempt}")
    return []

# ---------- 核心保存逻辑 ----------
def save(product_name, data, output_dir):
    if not data:
        return
    fname = f"{product_name}_{now_str()}.json"
    full_path = os.path.join(output_dir, fname)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f"已写入 {full_path}  共 {len(data)} 条")

# ---------- 抓取与异常抢救流程 ----------
def crawl_one_product(product, city_list, output_dir):
    code, name = product["code"], product["name"]
    logging.info(f"↓↓ 开始抓取【{name}】({code})")
    results = []
    
    try:
        for idx, city in enumerate(city_list, 1):
            cid, cname = city["id"], city["name"]
            offices = post_office_list(cid, code)
            for o in offices:
                # 顺手做一点数据清洗兜底，防止前端渲染出错
                o["cityName"] = cname
                o["cityId"] = cid
                o["productCode"] = code
                o["productName"] = name
                o["address"] = o.get("address", "地址暂无")
                o["longitude"] = o.get("longitude", "") 
                o["latitude"] = o.get("latitude", "")
            results.extend(offices)
            logging.info(f"[{idx:03}/{len(city_list)}] {cname:<10}  {len(offices):>3} 条")
            
    except Exception as e:
        # 捕获到不可预知的严重错误，记录详细的堆栈信息进文件
        error_msg = f"抓取【{name}】时发生严重中断: {e}"
        logging.error(error_msg, exc_info=True) 
        # 发送紧急通知
        bark_push("🚨 门店抓取中断", f"产品【{name}】抓取遇到意外错误，已抢救保存前 {len(results)} 条数据。详细报错已写入日志文件。")
        
    finally:
        # 无论如何，哪怕报错了，这行代码也一定会执行，实现数据落袋为安
        if results:
            save(name, results, output_dir)
            
    return results

# ---------- 启动入口 ----------
if __name__ == "__main__":
    # 1. 创建当天的存放目录
    today_dir = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(today_dir, exist_ok=True)
    
    # 2. 动态配置日志处理器，把 WARNING 级别以上的报错存入文本
    log_file = os.path.join(today_dir, "error.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.WARNING) 
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    logging.info(f"所有文件将被保存在目录: ./{today_dir}/")
    
    # 3. 开始执行
    CITIES = load_cities()
    total = 0
    for prod in PRODUCTS:
        rows = crawl_one_product(prod, CITIES, today_dir) 
        total += len(rows)

    bark_push("数据抓取完成", f"共抓取 {total} 条门店数据，保存在 {today_dir} 目录")
