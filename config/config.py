import os

class Config:
    # 基础配置
    BASE_DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "comic")
    
    # 并发配置
    CONCURRENT_LIMIT = 80
    
    # 浏览器配置
    CHROME_DRIVER_PATH = None  # 自动查找或手动设置
    HEADLESS = True
    
    # 请求配置
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'
    }
    
    # 超时配置
    TIMEOUT = 30
    
    # 重试配置
    RETRY_COUNT = 3

# 实例化配置对象
config = Config()
