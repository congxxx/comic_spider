import os
import time
import asyncio
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from ..spiders.base_spider import BaseSpider
from ..common.utils import download_image
from ..config.config import config

class CopyComicSpider(BaseSpider):
    """拷贝漫画爬虫"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.copymanga.org"
        self.browser = self._init_browser()
    
    def _init_browser(self):
        """初始化浏览器"""
        option = Options()
        if config.HEADLESS:
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        if config.CHROME_DRIVER_PATH:
            service = Service(config.CHROME_DRIVER_PATH)
            return webdriver.Chrome(service=service, options=option)
        else:
            return webdriver.Chrome(options=option)
    
    def search(self, keyword):
        """搜索漫画"""
        # 拷贝漫画网站的搜索功能实现
        search_url = f"{self.base_url}/search?q={keyword}"
        self.browser.get(search_url)
        time.sleep(2)
        
        page_text = self.browser.page_source
        res_xpath = etree.HTML(page_text)
        
        # 提取搜索结果
        comic_list = []
        # 这里需要根据实际网页结构调整XPath
        # 示例：comic_list = res_xpath.xpath('//div[@class="comic-item"]')
        
        return comic_list
    
    def get_chapters(self, comic_url):
        """获取漫画章节列表"""
        try:
            self.browser.get(comic_url)
            time.sleep(2)
            page_text = self.browser.page_source
            res_xpath = etree.HTML(page_text)
        except:
            self.browser.refresh()
            time.sleep(2)
            page_text = self.browser.page_source
            res_xpath = etree.HTML(page_text)
        
        # 提取章节信息
        half_detail_url_list = res_xpath.xpath('//div[2]/div[3]/div/div[2]/div/div[1]/ul[1]/a/@href')
        title_list = res_xpath.xpath('//*[@id="default全部"]/ul[1]/a/li/text()')
        
        chapters = []
        for i, (url, title) in enumerate(zip(half_detail_url_list, title_list)):
            chapter_url = self.base_url + url
            chapters.append({
                'index': i,
                'title': title,
                'url': chapter_url
            })
        
        return chapters
    
    def get_images(self, chapter_url):
        """获取章节图片列表"""
        self.browser.get(chapter_url)
        time.sleep(3)
        
        # 滚动页面加载图片
        for k in range(3):
            js = "return document.body.scrollHeight"
            new_height = self.browser.execute_script(js)
            for i in range(0, new_height, 350):
                time.sleep(0.03)
                self.browser.execute_script('window.scrollTo(0, %s)' % i)
        time.sleep(2)
        
        picture_text = self.browser.page_source
        pic_xpath = etree.HTML(picture_text)
        pic_url = pic_xpath.xpath('/html/body/div[2]/div/ul/li/img/@data-src')
        
        # 防止出现空url
        if len(pic_url) == 0:
            self.browser.get(chapter_url)
            time.sleep(3)
            for k in range(3):
                js = "return document.body.scrollHeight"
                new_height = self.browser.execute_script(js)
                for i in range(0, new_height, 350):
                    time.sleep(0.03)
                    self.browser.execute_script('window.scrollTo(0, %s)' % i)
            time.sleep(2)
            picture_text = self.browser.page_source
            pic_xpath = etree.HTML(picture_text)
            pic_url = pic_xpath.xpath('/html/body/div[2]/div/ul/li/img/@data-src')
        
        return pic_url
    
    async def download_chapter(self, chapter_info, comic_name):
        """下载章节"""
        chapter_title = chapter_info['title']
        chapter_url = chapter_info['url']
        
        print(f"开始下载章节: {chapter_title}")
        
        # 获取图片列表
        image_urls = self.get_images(chapter_url)
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
    
    def close(self):
        """关闭浏览器"""
        if hasattr(self, 'browser') and self.browser:
            self.browser.quit()
