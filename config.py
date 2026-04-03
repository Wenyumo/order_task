# config.py
# 请根据你的抓包信息替换以下内容
API_KEY = "oVw5lgBQ32mygdfZUvYuKAbYtm7DRN37"
USER_ID = "1551922328698482690"   # 你的钉钉userid
COOKIE_STR = "XSRF-TOKEN=eyJpdiI6IjNGXC9aOXN0QlQ1MVE0MmNyczJPRzNnPT0iLCJ2YWx1ZSI6IkRBNjBqbE9tRXI3YThId0o1a0VRYmx6NnQyYmZ4THViYUhYZmFzak1PUkxoWjdLbm9wMUp1TnI4UWEyOEpBckYiLCJtYWMiOiI5NDhmNjkxYTlhZWVhNjFhMjA2ZGVlYTlmOTc1M2UwODE4MmRjMTUyZjc3ZGM1MTQ4ZjdlZmFiMzYzMDcyOGY2In0%3D; logistics_session=eyJpdiI6Ikkxek9CNlwvaXBXblpvNTh5cXlsZW5nPT0iLCJ2YWx1ZSI6IkZhd2tFZmhJMjdwU2xkVklMZDZcLzAxNlBTZHY1cTR4M3hqbXJOSUpjU2hqRzFuSld3MTR2cFhkaGszYVA5VnkzIiwibWFjIjoiMTQ3Y2VmZmJhZWIxZDlkMDJiMjliOWQwNGQ4NDIyNmEzZmZiY2M2MThjODQ1NjRkOWJmZDBhNjdjNzI0ZDViMCJ9"
XSRF_TOKEN_HEADER = "eyJpdiI6IjNGXC9aOXN0QlQ1MVE0MmNyczJPRzNnPT0iLCJ2YWx1ZSI6IkRBNjBqbE9tRXI3YThId0o1a0VRYmx6NnQyYmZ4THViYUhYZmFzak1PUkxoWjdLbm9wMUp1TnI4UWEyOEpBckYiLCJtYWMiOiI5NDhmNjkxYTlhZWVhNjFhMjA2ZGVlYTlmOTc1M2UwODE4MmRjMTUyZjc3ZGM1MTQ4ZjdlZmFiMzYzMDcyOGY2In0="

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