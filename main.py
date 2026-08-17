#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import random
import logging
import csv
import re
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

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
#    {"name": "悦享涂氟", "code": "1000804"},
#    {"name": "悦享窝沟", "code": "1000805"},
#    {"name": "优享窝沟-限上海", "code": "1000480"},
    {"name": "优享洁牙-限上海", "code": "1000478"},
    {"name": "悦享洁牙", "code": "1000616"},
#    {"name": "惠享洁牙", "code": "1000642"},
#    {"name": "慧享洁牙", "code": "1000680"}, #注意，这个“慧”
#    {"name": "尊享洁牙-限上海", "code": "1000801"},
#    {"name": "精选洁牙", "code": "1000615"},
#    {"name": "臻享洁牙", "code": "1000628"},
#    {"name": "新享洁牙-带喷砂", "code": "1000876"},
#    {"name": "焕新洁牙-带喷砂", "code": "1000872"},
#    {"name": "【臻享权益】成人尊享喷砂洁牙套餐", "code": "1001558"},
    {"name": "尊享Only-限上海", "code": "1000871"},
 #   {"name": "乐享洁牙", "code": "1000625"},
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

# ---------- 工具 ----------
def now_str():
    return datetime.now().strftime("%m%d")

def fetch_cities(output_dir):
    """动态从接口拉取最新城市列表，保存 JSON，并摊平为 list 返回"""
    url = "https://ebkapi.17u.cn/hospital/api/common/getCities?name="
    
    # 调整 type 以适配该接口
    city_headers = HEADERS_TPL.copy()
    city_headers["type"] = "txMini"
    
    logging.info("正在从接口获取最新城市列表...")
    
    for attempt in range(1, 4):
        try:
            resp = requests.get(url, headers=city_headers, timeout=10)
            resp.raise_for_status()
            raw_data = resp.json()
            
            if raw_data.get("code") == "200":
                # 将接口原始返回的 JSON 落地保存
                city_json_path = os.path.join(output_dir, "cities.json")
                with open(city_json_path, "w", encoding="utf-8") as f:
                    json.dump(raw_data, f, ensure_ascii=False, indent=4)
                logging.info(f"✅ 城市数据已保存至: {city_json_path}")
                
                cities = []
                # 遍历字典（A, B, C...），把所有的城市合并到一个数组里
                for group in raw_data["data"].values():
                    cities.extend(group)
                logging.info(f"✅ 成功提取城市列表，共计 {len(cities)} 个城市。")
                return cities
            else:
                logging.warning(f"获取城市接口返回异常: {raw_data.get('message')} attempt={attempt}")
        except Exception as e:
            logging.warning(f"获取城市请求失败: {e} attempt={attempt}")
            time.sleep(1)
            
    logging.error("❌ 无法获取城市列表，脚本终止执行。")
    sys.exit(1)

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
            time.sleep(random.uniform(0.5, 2))
            resp = requests.post(url, headers=HEADERS_TPL, json=payload, timeout=12)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") == "200":
                return data.get("data", [])
            logging.warning(f"API 返回异常状态码/信息: {data.get('message')}  attempt={attempt}")
        except Exception as e:
            logging.warning(f"请求失败: {e}  attempt={attempt}")
    return []

def extract_region(address):
    """从地址字符串中尝试提取区或县"""
    if not address:
        return "未知区域"
    match = re.search(r'(?:省|市|自治区)([^省市]+?[区县])', address)
    if match:
        return match.group(1)
    fallback_match = re.search(r'([\u4e00-\u9fa5]{1,5}?[区县])', address)
    if fallback_match:
        return fallback_match.group(1)
    return "未知区域"

# ---------- 核心保存逻辑（同时保存 JSON 和 CSV） ----------
def save(product_name, data, output_dir):
    if not data:
        return
    
    store_count = len(data)
    base_name = f"{product_name}_{now_str()}"
    
    # 1. 保存 JSON
    json_fname = f"{base_name}.json"
    json_path = os.path.join(output_dir, json_fname)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f"已写入 JSON: {json_path}  共 {store_count} 条")

    # 2. 保存乐牙格式 CSV
    csv_fname = f"{base_name}_{store_count}.csv"
    csv_path = os.path.join(output_dir, csv_fname)
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['城市', '门店名称', '区域(组合后)', '地址', '评分(留空)', '标签(剔除)'])

            for store in data:
                city_name = store.get('cityName', '未知城市')
                store_name = store.get('name', '')
                address = store.get('address', '')

                if '市' not in city_name and city_name != '未知城市':
                    city_name = f"{city_name}市"

                region_name = extract_region(address)
                combined_region = f"{city_name}-{region_name}"

                writer.writerow([city_name, store_name, combined_region, address, '', ''])
                
        logging.info(f"已写入 CSV: {csv_path} (乐牙格式转换完毕)")
    except Exception as e:
        logging.error(f"写入 CSV 发生异常: {e}")

# ---------- 抓取与异常抢救流程 ----------
def crawl_one_product(product, city_list, output_dir, max_workers=10):
    code, name = product["code"], product["name"]
    
    if "限" in name:
        target_city_name = name.split("限")[-1].strip()
        city_list = [c for c in city_list if c["name"] == target_city_name]
        logging.info(f"产品【{name}】包含限定标识，已将抓取范围缩小至: {target_city_name}")

    logging.info(f"↓↓ 开始多线程抓取【{name}】({code})，并发数: {max_workers}")
    results = []
    
    def fetch_single_city(city):
        cid, cname = city["id"], city["name"]
        offices = post_office_list(cid, code)
        for o in offices:
            o["cityName"] = cname
            o["cityId"] = cid
            o["productCode"] = code
            o["productName"] = name
            o["address"] = o.get("address", "地址暂无")
            o["longitude"] = o.get("longitude", "") 
            o["latitude"] = o.get("latitude", "")
        return cname, offices
    
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_city = {executor.submit(fetch_single_city, city): city for city in city_list}
            
            completed_count = 0
            for future in as_completed(future_to_city):
                completed_count += 1
                try:
                    cname, offices = future.result()
                    if offices:
                        results.extend(offices)
                    logging.info(f"[{completed_count:03}/{len(city_list)}] {cname:<10}  {len(offices):>3} 条")
                except Exception as exc:
                    city_name = future_to_city[future]["name"]
                    logging.error(f"处理城市 {city_name} 时发生内部错误: {exc}")
                    
    except Exception as e:
        error_msg = f"抓取【{name}】时发生严重中断: {e}"
        logging.error(error_msg, exc_info=True) 
        bark_push("🚨 门店抓取中断", f"产品【{name}】抓取遇到意外错误，已抢救保存前 {len(results)} 条数据。")
        
    finally:
        if results:
            save(name, results, output_dir)
            
    return results

# ---------- 启动入口 ----------
if __name__ == "__main__":
    today_dir = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(today_dir, exist_ok=True)
    
    log_file = os.path.join(today_dir, "error.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.WARNING) 
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    logging.info(f"所有文件将被保存在目录: ./{today_dir}/")
    
    # 动态获取城市并保存到输出目录
    CITIES = fetch_cities(today_dir)
    total = 0
    WORKER_COUNT = 5 
    
    for prod in PRODUCTS:
        rows = crawl_one_product(prod, CITIES, today_dir, max_workers=WORKER_COUNT) 
        total += len(rows)

    bark_push("数据抓取完成", f"共抓取 {total} 条门店数据，保存在 {today_dir} 目录")
