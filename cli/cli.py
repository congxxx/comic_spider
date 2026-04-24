import click
import asyncio
from ..spiders.copy_comic_spider import CopyComicSpider
from ..spiders.zones_comic_spider import ZonesComicSpider
from ..spiders.dmhuah_spider import DmhuahSpider
from ..common.utils import zip_directory, delete_directory, is_image_empty
import os

@click.group()
def cli():
    """Comic Spider - 多网站漫画爬虫工具"""
    pass

@cli.command()
@click.option('--site', type=click.Choice(['copy_comic', 'zones_comic', 'dmhuah'], case_sensitive=False), required=True, help='选择爬虫网站')
@click.option('--url', help='漫画详情页URL')
@click.option('--keyword', help='搜索关键词')
@click.option('--comic-name', help='漫画名称')
@click.option('--start-chapter', type=int, default=0, help='开始章节索引')
@click.option('--end-chapter', type=int, default=-1, help='结束章节索引')
@click.option('--zip', is_flag=True, help='是否打包成压缩包')
def download(site, url, keyword, comic_name, start_chapter, end_chapter, zip):
    """下载漫画"""
    async def main():
        # 选择爬虫
        if site == 'copy_comic':
            spider = CopyComicSpider()
        elif site == 'zones_comic':
            spider = ZonesComicSpider()
        elif site == 'dmhuah':
            spider = DmhuahSpider()
        else:
            click.echo('不支持的网站')
            return
        
        try:
            # 如果提供了关键词，先搜索
            if keyword:
                click.echo(f'正在搜索漫画: {keyword}')
                comics = spider.search(keyword)
                
                if not comics:
                    click.echo('未找到相关漫画')
                    return
                
                # 显示搜索结果
                click.echo('搜索结果:')
                for comic in comics:
                    click.echo(f"{comic['index']}. {comic['title']}")
                
                # 选择漫画
                choice = click.prompt('请选择漫画序号', type=int, default=1)
                if choice < 1 or choice > len(comics):
                    click.echo('无效的选择')
                    return
                
                comic = comics[choice - 1]
                url = comic['url']
                if not comic_name:
                    comic_name = comic['title']
            
            # 确保提供了URL和漫画名称
            if not url:
                click.echo('请提供漫画详情页URL')
                return
            if not comic_name:
                click.echo('请提供漫画名称')
                return
            
            # 获取章节列表
            click.echo(f'正在获取漫画章节: {comic_name}')
            chapters = spider.get_chapters(url)
            click.echo(f'共找到 {len(chapters)} 个章节')
            
            # 确定章节范围
            if end_chapter == -1:
                end_chapter = len(chapters)
            chapters_to_download = chapters[start_chapter:end_chapter]
            
            # 下载章节
            click.echo(f'开始下载 {len(chapters_to_download)} 个章节')
            success_count = 0
            for chapter in chapters_to_download:
                success = await spider.download_chapter(chapter, comic_name)
                if success:
                    success_count += 1
            
            click.echo(f'下载完成，成功 {success_count}/{len(chapters_to_download)}')
            
            # 打包成压缩包
            if zip:
                comic_path = os.path.join(spider.download_path, comic_name)
                zip_path = f"{comic_path}.zip"
                zip_directory(comic_path, zip_path)
                delete_directory(comic_path)
                click.echo(f'已打包为: {zip_path}')
                
        finally:
            # 关闭爬虫资源
            if hasattr(spider, 'close'):
                spider.close()
    
    asyncio.run(main())

@cli.command()
def list_sites():
    """列出支持的网站"""
    sites = [
        {'name': 'copy_comic', 'url': 'https://www.copymanga.org'},
        {'name': 'zones_comic', 'url': 'http://www.zerobywgeat.com'},
        {'name': 'dmhuah', 'url': 'https://m.dmhuah.com'}
    ]
    
    click.echo('支持的网站:')
    for site in sites:
        click.echo(f"- {site['name']}: {site['url']}")

if __name__ == '__main__':
    cli()
