# main.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime, timedelta
from config import ROUTES
from api import get_vehicle_list, get_reserved_seats, create_order

class ConfigWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("配置设置")
        self.window.geometry("800x600")
        self.window.resizable(True, True)

        # 默认配置值
        self.default_config = {
            "API_KEY": "oVw5lgBQ32mygdfZUvYuKAbYtm7DRN37",
            "USER_ID": "1551922328698482690",
            "COOKIE_STR": "XSRF-TOKEN=eyJpdiI6IjNGXC9aOXN0QlQ1MVE0MmNyczJPRzNnPT0iLCJ2YWx1ZSI6IkRBNjBqbE9tRXI3YThId0o1a0VRYmx6NnQyYmZ4THViYUhYZmFzak1PUkxoWjdLbm9wMUp1TnI4UWEyOEpBckYiLCJtYWMiOiI5NDhmNjkxYTlhZWVhNjFhMjA2ZGVlYTlmOTc1M2UwODE4MmRjMTUyZjc3ZGM1MTQ4ZjdlZmFiMzYzMDcyOGY2In0%3D; logistics_session=eyJpdiI6Ikkxek9CNlwvaXBXblpvNTh5cXlsZW5nPT0iLCJ2YWx1ZSI6IkZhd2tFZmhJMjdwU2xkVklMZDZcLzAxNlBTZHY1cTR4M3hqbXJOSUpjU2hqRzFuSld3MTR2cFhkaGszYVA5VnkzIiwibWFjIjoiMTQ3Y2VmZmJhZWIxZDlkMDJiMjliOWQwNGQ4NDIyNmEzZmZiY2M2MThjODQ1NjRkOWJmZDBhNjdjNzI0ZDViMCJ9",
            "XSRF_TOKEN_HEADER": "eyJpdiI6IjNGXC9aOXN0QlQ1MVE0MmNyczJPRzNnPT0iLCJ2YWx1ZSI6IkRBNjBqbE9tRXI3YThId0o1a0VRYmx6NnQyYmZ4THViYUhYZmFzak1PUkxoWjdLbm9wMUp1TnI4UWEyOEpBckYiLCJtYWMiOiI5NDhmNjkxYTlhZWVhNjFhMjA2ZGVlYTlmOTc1M2UwODE4MmRjMTUyZjc3ZGM1MTQ4ZjdlZmFiMzYzMDcyOGY2In0="
        }

        self.create_widgets()
        self.load_current_config()

    def create_widgets(self):
        # 配置输入区域
        config_frame = ttk.LabelFrame(self.window, text="配置参数", padding=10)
        config_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # API_KEY
        ttk.Label(config_frame, text="API_KEY：").grid(row=0, column=0, sticky="w", pady=5)
        self.api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(config_frame, textvariable=self.api_key_var, width=80)
        api_key_entry.grid(row=0, column=1, pady=5, sticky="w")

        # USER_ID
        ttk.Label(config_frame, text="USER_ID：").grid(row=1, column=0, sticky="w", pady=5)
        self.user_id_var = tk.StringVar()
        user_id_entry = ttk.Entry(config_frame, textvariable=self.user_id_var, width=80)
        user_id_entry.grid(row=1, column=1, pady=5, sticky="w")

        # COOKIE_STR
        ttk.Label(config_frame, text="COOKIE_STR：").grid(row=2, column=0, sticky="w", pady=5)
        self.cookie_var = tk.StringVar()
        cookie_entry = ttk.Entry(config_frame, textvariable=self.cookie_var, width=80)
        cookie_entry.grid(row=2, column=1, pady=5, sticky="w")

        # XSRF_TOKEN_HEADER
        ttk.Label(config_frame, text="XSRF_TOKEN_HEADER：").grid(row=3, column=0, sticky="w", pady=5)
        self.xsrf_var = tk.StringVar()
        xsrf_entry = ttk.Entry(config_frame, textvariable=self.xsrf_var, width=80)
        xsrf_entry.grid(row=3, column=1, pady=5, sticky="w")

        # 按钮区域
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="保存配置", command=self.save_config).pack(side="left", padx=10)
        ttk.Button(button_frame, text="恢复默认", command=self.restore_default).pack(side="left", padx=10)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side="right", padx=10)

    def load_current_config(self):
        # 从config模块导入当前配置
        try:
            from config import API_KEY, USER_ID, COOKIE_STR, XSRF_TOKEN_HEADER
            self.api_key_var.set(API_KEY)
            self.user_id_var.set(USER_ID)
            self.cookie_var.set(COOKIE_STR)
            self.xsrf_var.set(XSRF_TOKEN_HEADER)
        except ImportError:
            # 如果导入失败，使用默认值
            self.api_key_var.set(self.default_config["API_KEY"])
            self.user_id_var.set(self.default_config["USER_ID"])
            self.cookie_var.set(self.default_config["COOKIE_STR"])
            self.xsrf_var.set(self.default_config["XSRF_TOKEN_HEADER"])

    def save_config(self):
        # 保存配置到config.py文件
        config_content = f"""# config.py
# 请根据你的抓包信息替换以下内容
API_KEY = "{self.api_key_var.get()}"
USER_ID = "{self.user_id_var.get()}"   # 你的钉钉userid
COOKIE_STR = "{self.cookie_var.get()}"
XSRF_TOKEN_HEADER = "{self.xsrf_var.get()}"

# 路线列表（显示顺序）
ROUTES = [
    "中关村校区->良乡校区",
    "良乡校区->中关村校区",
    "中关村校区->西山校区",
    "西山校区->中关村校区",
    "中关村校区->回龙观",
    "回龙观->中关村校区",
    "中关村校区->房山分校阎村",
    "房山分校阎村->中关村校区",
    "良乡校区->回龙观",
    "回龙观->良乡校区"
]

# 请求配置
REQUEST_TIMEOUT = 10          # 请求超时秒数
SEAT_REFRESH_INTERVAL = 5     # 座位刷新间隔（秒）
MAX_RETRY_BEFORE_SALE = 3     # 开售前最大重试次数（用于验证Cookie是否有效）
"""

        try:
            with open("config.py", "w", encoding="utf-8") as f:
                f.write(config_content)
            tk.messagebox.showinfo("成功", "配置保存成功！")
        except Exception as e:
            tk.messagebox.showerror("错误", f"保存配置失败：{str(e)}")

    def restore_default(self):
        # 恢复默认配置
        self.api_key_var.set(self.default_config["API_KEY"])
        self.user_id_var.set(self.default_config["USER_ID"])
        self.cookie_var.set(self.default_config["COOKIE_STR"])
        self.xsrf_var.set(self.default_config["XSRF_TOKEN_HEADER"])
        tk.messagebox.showinfo("成功", "已恢复默认配置！")

class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("北理班车抢票助手")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # 状态变量
        self.selected_route = tk.StringVar()
        self.selected_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.vehicles = []          # 班次列表
        self.selected_vehicle = None # 选中的班次字典
        self.running = False         # 抢票线程运行标志
        self.stop_flag = False       # 停止标志

        self.create_widgets()

    def create_widgets(self):
        # 顶部框架：路线选择
        top_frame = ttk.LabelFrame(self.root, text="1. 选择路线", padding=10)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="路线：").grid(row=0, column=0, sticky="w")
        route_combo = ttk.Combobox(top_frame, textvariable=self.selected_route, values=ROUTES, width=40)
        route_combo.grid(row=0, column=1, padx=5, pady=5)
        route_combo.current(0)

        ttk.Label(top_frame, text="日期：").grid(row=0, column=2, sticky="w", padx=(20,0))
        date_entry = ttk.Entry(top_frame, textvariable=self.selected_date, width=12)
        date_entry.grid(row=0, column=3, padx=5)
        ttk.Button(top_frame, text="查询班次", command=self.query_vehicles).grid(row=0, column=4, padx=10)
        ttk.Button(top_frame, text="配置设置", command=self.open_config_window).grid(row=0, column=5, padx=10)

        # 班次列表显示
        vehicle_frame = ttk.LabelFrame(self.root, text="2. 选择班次", padding=10)
        vehicle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("序号", "发车时间", "学生价", "教师价", "最大座位数", "班次ID")
        self.tree = ttk.Treeview(vehicle_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column("班次ID", width=150)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(vehicle_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_vehicle_select)

        # 操作按钮及状态
        action_frame = ttk.LabelFrame(self.root, text="3. 抢票控制", padding=10)
        action_frame.pack(fill="x", padx=10, pady=5)

        self.start_button = ttk.Button(action_frame, text="开始抢票（自动等待开售）", command=self.start_booking, state="disabled")
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(action_frame, text="停止", command=self.stop_booking, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        self.status_label = ttk.Label(action_frame, text="状态：未选择班次", foreground="blue")
        self.status_label.pack(side="left", padx=20)

        # 日志区域
        log_frame = ttk.LabelFrame(self.root, text="运行日志", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, state="normal")
        self.log_text.pack(fill="both", expand=True)

    def log(self, msg):
        """在日志区域添加时间戳信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def query_vehicles(self):
        """查询班次并显示在表格中"""
        route = self.selected_route.get()
        date = self.selected_date.get()
        if not route or not date:
            messagebox.showwarning("提示", "请选择路线和日期")
            return

        self.log(f"正在查询 {date} {route} 的班次...")
        # 清空原有显示
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.vehicles = []
        self.selected_vehicle = None
        self.start_button.config(state="disabled")
        self.status_label.config(text="状态：未选择班次")

        result = get_vehicle_list(date, route)
        if isinstance(result, dict) and "error" in result:
            self.log(f"查询失败：{result['error']}")
            messagebox.showerror("错误", f"查询失败：{result['error']}\n请检查Cookie是否过期")
            return

        if not result:
            self.log("未查询到任何班次")
            return

        self.vehicles = result
        for idx, v in enumerate(result, 1):
            # 使用班次ID作为iid，方便直接定位
            iid = v.get("id")
            self.tree.insert("", tk.END, iid=iid, values=(
                idx,
                v.get("origin_time", "未知"),
                v.get("student_ticket_price", "N/A"),
                v.get("teacher_ticket_price", "N/A"),
                v.get("reservation_num_able", "?"),
                v.get("id", "")
            ))
        self.log(f"查询成功，共 {len(result)} 个班次")

    def on_vehicle_select(self, event):
        """用户选中班次后记录选中项"""
        selection = self.tree.selection()
        if not selection:
            return
        # selection[0] 就是插入时的 iid（即班次ID）
        selected_id = selection[0]
        # 从 self.vehicles 中查找匹配的班次
        for v in self.vehicles:
            if v.get("id") == selected_id:
                self.selected_vehicle = v
                self.start_button.config(state="normal")
                self.status_label.config(text=f"状态：已选择 {v.get('origin_time')} 班次")
                self.log(f"选中班次：{v.get('origin_time')} (ID:{selected_id})")
                return
        # 如果没找到（极少情况），尝试从表格的values中获取ID
        item = self.tree.item(selection[0])
        values = item['values']
        if values and len(values) >= 6:
            vehicle_id = values[5]  # 最后一列是班次ID
            for v in self.vehicles:
                if v.get("id") == vehicle_id:
                    self.selected_vehicle = v
                    self.start_button.config(state="normal")
                    self.status_label.config(text=f"状态：已选择 {v.get('origin_time')} 班次")
                    self.log(f"选中班次：{v.get('origin_time')} (ID:{vehicle_id})")
                    return
        self.log("选中班次失败，请重试")

    def start_booking(self):
        """开始抢票线程"""
        if not self.selected_vehicle:
            messagebox.showwarning("提示", "请先选择一个班次")
            return
        if self.running:
            messagebox.showinfo("提示", "抢票已在运行中")
            return

        self.running = True
        self.stop_flag = False
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("启动抢票线程...")
        threading.Thread(target=self.booking_worker, daemon=True).start()

    def stop_booking(self):
        """停止抢票"""
        self.stop_flag = True
        self.log("正在停止抢票...")

    def booking_worker(self):
        """优化版：开票前预查询座位，开票瞬间直接下单"""
        vehicle = self.selected_vehicle
        vehicle_id = vehicle.get("id")
        origin_time_str = vehicle.get("origin_time")
        date = self.selected_date.get()
        # 计算发车时间和开售时间
        try:
            departure = datetime.strptime(f"{date} {origin_time_str}", "%Y-%m-%d %H:%M")
        except Exception as e:
            self.log(f"时间解析错误：{e}")
            self.stop_booking_done()
            return
        sale_time = departure - timedelta(hours=1)
        now = datetime.now()

        # 等待开售时间
        if now < sale_time:
            wait_seconds = (sale_time - now).total_seconds()
            self.log(f"当前时间 {now.strftime('%H:%M:%S')}，开售时间 {sale_time.strftime('%H:%M:%S')}")
            self.log(f"等待 {wait_seconds:.2f} 秒...")
            # 等待到开售前 2 秒
            pre_wait = max(0, wait_seconds - 2)
            if pre_wait > 0:
                time.sleep(pre_wait)
            # 开售前 2 秒：预先查询一次座位
            self.log("开售前预查询座位信息...")
            seat_result = get_reserved_seats(vehicle_id, date)
            if not seat_result.get("success"):
                self.log(f"预查询座位失败：{seat_result.get('error')}")
            else:
                reserved = set(seat_result["reserved"])
                disabled = set(seat_result["disabled"])
                max_seat = vehicle.get("reservation_num_able", 51)
                self.cached_free_seats = []
                for seat in range(1, max_seat + 1):
                    if seat not in reserved and seat not in disabled:
                        self.cached_free_seats.append(seat)
                self.log(f"预查询到 {len(self.cached_free_seats)} 个空闲座位")
            # 精确等待最后 2 秒（使用忙等待提高精度）
            self.log("进入最后冲刺等待...")
            while datetime.now() < sale_time:
                time.sleep(0.001)  # 1ms 轮询，高精度
            self.log("开售时间到！立即抢票！")
        else:
            self.log("当前时间已过开售时间，立即开始抢票！")
            # 没有预查询，直接后续查询
            self.cached_free_seats = []

        # 抢票循环
        seat_number = None
        retry_count = 0
        # 先尝试使用缓存的空闲座位（如果有）
        if self.cached_free_seats:
            self.log(f"使用预缓存座位列表，第一个候选座位：{self.cached_free_seats[0]}")
        else:
            self.cached_free_seats = []

        while not self.stop_flag:
            # 如果有缓存座位且还没用完，直接取用
            if self.cached_free_seats:
                seat_number = self.cached_free_seats.pop(0)
                self.log(f"尝试使用缓存座位 {seat_number} 下单...")
            else:
                # 缓存用完了，实时获取座位
                self.log("正在实时获取空闲座位...")
                seat_result = get_reserved_seats(vehicle_id, date)
                if not seat_result.get("success"):
                    self.log(f"获取座位失败：{seat_result.get('error')}")
                    if "Cookie" in seat_result.get("error", ""):
                        self.log("Cookie可能已过期，请重新获取并更新config.py后重启程序")
                        break
                    time.sleep(0.2)
                    continue
                reserved = set(seat_result["reserved"])
                disabled = set(seat_result["disabled"])
                max_seat = vehicle.get("reservation_num_able", 51)
                free_seats = [s for s in range(1, max_seat + 1) if s not in reserved and s not in disabled]
                if not free_seats:
                    self.log("无空闲座位，等待0.2秒后重试")
                    time.sleep(0.2)
                    continue
                seat_number = free_seats[0]
                # 将剩余座位缓存起来（可选）
                self.cached_free_seats = free_seats[1:]

            # 构造Referer
            referer = f"http://hqapp1.bit.edu.cn/newbanche/choose?id={vehicle_id}&shuttleType=3&serviceTime=1,2,3,4,5&originTime={origin_time_str.replace(':', '%3A')}&price={vehicle.get('student_ticket_price', '')}"
            order_result = create_order(vehicle_id, date, seat_number, referer)
            if order_result.get("code") == "1":
                self.log(f"抢票成功！订单已创建，座位号 {seat_number}。请尽快登录系统支付。")
                self.root.bell()
                break
            else:
                error_msg = order_result.get("message", "未知错误")
                self.log(f"下单失败（座位{seat_number}）：{error_msg}")
                if "已预约" in error_msg or "已被预约" in error_msg:
                    # 座位被占，继续使用下一个缓存座位（如果有）
                    self.log("座位已被占，尝试下一个候选座位")
                    continue
                elif "未开启预约" in error_msg or "发车前一个小时" in error_msg:
                    self.log("尚未到可预约时间，等待0.5秒后重试")
                    time.sleep(0.5)
                    continue
                else:
                    retry_count += 1
                    if retry_count > 10:
                        self.log("连续失败次数过多，停止抢票")
                        break
                    time.sleep(0.2)
        else:
            self.log("抢票已停止")
        self.stop_booking_done()

    def stop_booking_done(self):
        """清理抢票结束状态"""
        self.running = False
        self.stop_flag = False
        self.start_button.config(state="normal" if self.selected_vehicle else "disabled")
        self.stop_button.config(state="disabled")
        self.log("抢票线程已结束")

    def open_config_window(self):
        """打开配置设置窗口"""
        ConfigWindow(self.root)

def main():
    root = tk.Tk()
    app = TicketApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
