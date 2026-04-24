import os
import time
import re
import asyncio
import requests
from lxml import etree
from ..spiders.base_spider import BaseSpider
from ..common.utils import download_image
from ..config.config import config

class ZonesComicSpider(BaseSpider):
    """Zero搬运网漫画爬虫"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "http://www.zerobywgeat.com"
    
    def search(self, keyword):
        """搜索漫画"""
        url = f'{self.base_url}/plugin.php?id=jameson_manhua&a=search&c=index&keyword={keyword}'
        response = requests.get(url=url, headers=self.headers)
        resp_xpath = etree.HTML(response.text)
        
        title_list = resp_xpath.xpath('//*[@id="jameson_manhua"]/div/div[1]/div[1]/a/div[2]/p/text()')
        url_list = resp_xpath.xpath('//*[@id="jameson_manhua"]/div/div[1]/a/@href')
        
        comics = []
        for i, (title, url) in enumerate(zip(title_list[:5], url_list[:5])):
            comic_url = f'{self.base_url}/{url}'
            comics.append({
                'index': i + 1,
                'title': title,
                'url': comic_url
            })
        
        return comics
    
    def get_chapters(self, comic_url):
        """获取漫画章节列表"""
        response = requests.get(url=comic_url, headers=self.headers)
        resp_xpath = etree.HTML(response.text)
        
        # 提取标题和章节
        str_title = resp_xpath.xpath("*//title/text()")[0]
        title = str_title.split("【")[0]
        
        chapter_list = resp_xpath.xpath('//*[@id="jameson_manhua"]/div[1]/div[1]/div[3]/div/a/text()')
        chapter_urls = resp_xpath.xpath('//*[@id="jameson_manhua"]/div[1]/div[1]/div[3]/div/a/@href')
        
        # 提取图片URL前缀
        pic = resp_xpath.xpath('//*[@id="jameson_manhua"]/div[1]/div[1]/div[1]/div[1]/img/@src')[0].split("/")
        pic_url_prefix = "/".join(pic[:-2])
        
        chapters = []
        for i, (chapter_title, chapter_url) in enumerate(zip(chapter_list, chapter_urls)):
            chapters.append({
                'index': i,
                'title': chapter_title,
                'url': chapter_url,
                'pic_url_prefix': pic_url_prefix
            })
        
        return chapters
    
    def get_images(self, chapter_info):
        """获取章节图片列表"""
        chapter_title = chapter_info['title']
        pic_url_prefix = chapter_info['pic_url_prefix']
        
        # 处理生肉标记
        if '生肉' in chapter_title:
            chapter_title = re.findall(r"\d+", chapter_title)[0] + 'sheng'
        
        # 构造图片URL
        suffix = ['', '.jpg', '.png']
        pic_list = []
        
        for flag in range(3):
            juge = [
                f'{pic_url_prefix}/{chapter_title}/001{suffix[flag]}',
                f'{pic_url_prefix}/{chapter_title}/01{suffix[flag]}',
                f'{pic_url_prefix}/{chapter_title}/1{suffix[flag]}'
            ]
            
            for url in juge:
                if requests.get(url=url, headers=self.headers).status_code == 200:
                    # 确定数字格式
                    if url == juge[0]:
                        format_str = '{:03d}'
                    elif url == juge[1]:
                        format_str = '{:02d}'
                    else:
                        format_str = '{}'
                    
                    # 生成图片URL列表
                    i = 1
                    while True:
                        img_url = f'{pic_url_prefix}/{chapter_title}/{format_str.format(i)}{suffix[flag]}'
                        if requests.get(url=img_url, headers=self.headers).status_code != 200:
                            break
                        pic_list.append(img_url)
                        i += 1
                    
                    # 尝试其他格式
                    for other_flag in range(3):
                        if other_flag != flag:
                            i = 1
                            while True:
                                img_url = f'{pic_url_prefix}/{chapter_title}/{format_str.format(i)}{suffix[other_flag]}'
                                if requests.get(url=img_url, headers=self.headers).status_code != 200:
                                    break
                                pic_list.append(img_url)
                                i += 1
                    
                    break
        
        return pic_list
    
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
