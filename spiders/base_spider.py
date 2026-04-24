import os
from abc import ABC, abstractmethod
from ..common.utils import ensure_dir, create_semaphore
from ..config.config import config

class BaseSpider(ABC):
    """基础爬虫类，定义通用接口"""
    
    def __init__(self):
        self.download_path = config.BASE_DOWNLOAD_PATH
        self.headers = config.HEADERS
        self.semaphore = create_semaphore(config.CONCURRENT_LIMIT)
    
    @abstractmethod
    def search(self, keyword):
        """搜索漫画"""
        pass
    
    @abstractmethod
    def get_chapters(self, comic_url):
        """获取漫画章节列表"""
        pass
    
    @abstractmethod
    def get_images(self, chapter_url):
        """获取章节图片列表"""
        pass
    
    @abstractmethod
    async def download_chapter(self, chapter_info, comic_name):
        """下载章节"""
        pass
    
    def get_download_path(self, comic_name, chapter_name):
        """获取下载路径"""
        return os.path.join(self.download_path, comic_name, chapter_name)
