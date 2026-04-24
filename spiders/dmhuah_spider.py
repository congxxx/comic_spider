import os
import time
import asyncio
import requests
from lxml import etree
from ..spiders.base_spider import BaseSpider
from ..common.utils import download_image
from ..config.config import config

class DmhuahSpider(BaseSpider):
    """dmhuah漫画爬虫"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://m.dmhuah.com"
        self.image_base_url = "https://res5.laomo365.com/image/view"
    
    def search(self, keyword):
        """搜索漫画"""
        # dmhuah网站的搜索功能实现
        search_url = f"{self.base_url}/search?q={keyword}"
        response = requests.get(search_url, headers=self.headers)
        resp_xpath = etree.HTML(response.text)
        
        # 提取搜索结果
        comic_list = []
        # 这里需要根据实际网页结构调整XPath
        # 示例：comic_list = resp_xpath.xpath('//div[@class="comic-item"]')
        
        return comic_list
    
    def get_chapters(self, comic_url):
        """获取漫画章节列表"""
        response = requests.get(url=comic_url, headers=self.headers)
        resp_xpath = etree.HTML(response.text)
        
        # 提取章节信息
        title_list = resp_xpath.xpath('//*[@id="chapter-list-1"]/li/a/span/text()')
        detail_list = resp_xpath.xpath('//*[@id="chapter-list-1"]/li/a/@href')
        detail_list = [f'{self.base_url}{i}' for i in detail_list]
        
        chapters = []
        for i, (title, url) in enumerate(zip(title_list, detail_list)):
            chapters.append({
                'index': i,
                'title': title,
                'url': url
            })
        
        return chapters
    
    def get_images(self, chapter_info):
        """获取章节图片列表"""
        chapter_url = chapter_info['url']
        chapter_id = chapter_url.split("/")[-1].split(".")[0]
        
        # 构造图片URL
        pic_url_list = []
        index = 0
        
        while True:
            img_url = f'{self.image_base_url}/{chapter_id}/{index}.webp'
            if requests.get(url=img_url, headers=self.headers).status_code != 200:
                break
            pic_url_list.append(img_url)
            index += 1
        
        return pic_url_list
    
    async def download_chapter(self, chapter_info, comic_name):
        """下载章节"""
        chapter_title = chapter_info['title']
        
        print(f"开始下载章节: {chapter_title}")
        
        # 获取图片列表
        image_urls = self.get_images(chapter_info)
        print(f"章节 {chapter_title} 共有 {len(image_urls)} 张图片")
        
        # 下载图片
        tasks = []
        for i, img_url in enumerate(image_urls):
            save_path = os.path.join(self.download_path, comic_name, chapter_title, f"{i+1}.jpg")
            task = download_image(img_url, save_path, self.headers, self.semaphore)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        success_count = sum(results)
        print(f"章节 {chapter_title} 下载完成，成功 {success_count}/{len(results)}")
        
        return success_count == len(results)
