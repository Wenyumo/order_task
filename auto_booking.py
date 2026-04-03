# auto_booking.py
import time
from datetime import datetime, timedelta
from api import get_vehicle_list, get_reserved_seats, create_order

def main():
    print("=== 北理班车自动抢票开始 ===")
    
    # 固定配置
    route = "中关村校区->良乡校区"  # 固定路线
    target_time = "21:10"  # 固定发车时间（晚上9:10）
    date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"查询日期：{date}")
    print(f"查询路线：{route}")
    print(f"目标班次：{target_time}")
    
    # 1. 查询班次
    print("正在查询班次...")
    vehicles = get_vehicle_list(date, route)
    if not vehicles:
        print("❌ 未查询到班次")
        return
    
    # 2. 筛选9:10的班次
    target_vehicle = None
    for vehicle in vehicles:
        origin_time = vehicle.get("origin_time", "")
        if origin_time == target_time:
            target_vehicle = vehicle
            break
    
    if not target_vehicle:
        print(f"❌ 未找到 {target_time} 的班次")
        return
    
    vehicle_id = target_vehicle.get("id")
    origin_time_str = target_vehicle.get("origin_time")
    print(f"选中班次：{origin_time_str} (ID: {vehicle_id})")
    
    # 3. 计算开售时间（发车前1小时）
    try:
        departure = datetime.strptime(f"{date} {origin_time_str}", "%Y-%m-%d %H:%M")
        sale_time = departure - timedelta(hours=1)
        now = datetime.now()
        print(f"发车时间：{departure.strftime('%Y-%m-%d %H:%M')}")
        print(f"开售时间：{sale_time.strftime('%Y-%m-%d %H:%M')}")
    except Exception as e:
        print(f"❌ 时间解析错误：{e}")
        return
    
    # 4. 等待开售
    if now < sale_time:
        wait_seconds = (sale_time - now).total_seconds()
        print(f"⏰ 等待 {wait_seconds:.2f} 秒到开售时间...")
        time.sleep(wait_seconds)
    print("🎉 开售时间到！开始抢票！")
    
    # 5. 抢票循环
    retry_count = 0
    max_retries = 50  # 最多尝试50次
    
    while retry_count < max_retries:
        retry_count += 1
        print(f"尝试第 {retry_count} 次...")
        
        # 获取空闲座位
        seat_result = get_reserved_seats(vehicle_id, date)
        if not seat_result.get("success"):
            print(f"❌ 获取座位失败：{seat_result.get('error')}")
            time.sleep(0.3)
            continue
        
        # 筛选空闲座位
        reserved = set(seat_result["reserved"])
        disabled = set(seat_result["disabled"])
        max_seat = target_vehicle.get("reservation_num_able", 51)
        free_seats = [s for s in range(1, max_seat + 1) if s not in reserved and s not in disabled]
        
        if not free_seats:
            print("❌ 无空闲座位，等待重试...")
            time.sleep(0.3)
            continue
        
        # 选择第一个空闲座位
        seat_number = free_seats[0]
        print(f"✅ 找到空闲座位：{seat_number}")
        
        # 构造 referer
        referer = f"http://hqapp1.bit.edu.cn/newbanche/choose?id={vehicle_id}&shuttleType=3&serviceTime=1,2,3,4,5&originTime={origin_time_str.replace(':', '%3A')}&price={target_vehicle.get('student_ticket_price', '')}"
        
        # 下单
        order_result = create_order(vehicle_id, date, seat_number, referer)
        if order_result.get("code") == "1":
            print(f"🎉 抢票成功！座位号：{seat_number}")
            print("请尽快登录系统支付！")
            return
        else:
            error_msg = order_result.get("message", "未知错误")
            print(f"❌ 下单失败：{error_msg}")
            time.sleep(0.2)
    
    print("❌ 抢票失败：尝试次数过多")

if __name__ == "__main__":
    main()
