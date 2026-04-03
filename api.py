# api.py
import requests
import time
import hashlib
from datetime import datetime
from config import API_KEY, USER_ID, COOKIE_STR, XSRF_TOKEN_HEADER, REQUEST_TIMEOUT

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def generate_apitoken(apitime):
    """生成请求签名"""
    step1 = md5(API_KEY + str(apitime))
    step2 = md5(step1)
    return step2

def get_headers(apitime, referer=None):
    """构造公共请求头"""
    headers = {
        "Host": "hqapp1.bit.edu.cn",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "com.alibaba.android.rimet.bitding",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 16; zh-CN; 2510DRK44C Build/BP2A.250605.031.A3) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 UWS/5.12.11.0 Mobile Safari/537.36 AliApp(DingTalk/8.1.10.1)",
        "Origin": "http://hqapp1.bit.edu.cn",
        "Cookie": COOKIE_STR,
        "X-XSRF-TOKEN": XSRF_TOKEN_HEADER,
        "apitime": str(apitime),
        "apitoken": generate_apitoken(apitime),
    }
    if referer:
        headers["Referer"] = referer
    return headers

def get_vehicle_list(date, address):
    """获取班次列表"""
    url = "http://hqapp1.bit.edu.cn/vehicle/get-list"
    apitime = int(time.time() * 1000)
    headers = get_headers(apitime, referer="http://hqapp1.bit.edu.cn/newbanche/home")
    params = {
        "page": 1,
        "limit": 50,
        "date": date,
        "address": address,
        "userid": USER_ID
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "0":
                return data.get("data", [])
            else:
                return {"error": data.get("message", "未知错误")}
        else:
            return {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_reserved_seats(vehicle_id, date):
    """获取座位布局（已占座位列表）"""
    url = "http://hqapp1.bit.edu.cn/vehicle/get-reserved-seats"
    apitime = int(time.time() * 1000)
    referer = f"http://hqapp1.bit.edu.cn/newbanche/choose?id={vehicle_id}&shuttleType=3&serviceTime=1,2,3,4,5"
    headers = get_headers(apitime, referer=referer)
    params = {
        "id": vehicle_id,
        "date": date,
        "userid": USER_ID
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "1":
                seat_data = data.get("data", {})
                reserved = [int(s) for s in seat_data.get("reserved_seat_number", []) if s.isdigit()]
                disabled = seat_data.get("disable_seat", [])
                return {"reserved": reserved, "disabled": disabled, "success": True}
            else:
                return {"success": False, "error": data.get("message", "获取座位失败")}
        else:
            return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_order(vehicle_id, date, seat_number, referer_url):
    """创建订单（抢票）"""
    url = "http://hqapp1.bit.edu.cn/vehicle/create-order"
    apitime = int(time.time() * 1000)
    headers = get_headers(apitime, referer=referer_url)
    data = {
        "id": vehicle_id,
        "date": date,
        "seat_number": str(seat_number),
        "userid": USER_ID
    }
    try:
        resp = requests.post(url, headers=headers, data=data, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"code": str(resp.status_code), "message": resp.text}
    except Exception as e:
        return {"code": "ERROR", "message": str(e)}