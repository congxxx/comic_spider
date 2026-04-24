import os
import time
import asyncio
import aiohttp
import aiofiles
from aiohttp import ClientTimeout
import numpy as np
import shutil
import zipfile

# 并发控制
def create_semaphore(limit=80):
    return asyncio.Semaphore(limit)

# 检查目录是否存在，不存在则创建
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 异步下载图片
async def download_image(url, save_path, headers=None, semaphore=None):
    timeout = ClientTimeout(total=350)
    conn = aiohttp.TCPConnector(limit=64, ssl=False)
    
    if semaphore:
        async with semaphore:
            return await _download_image(url, save_path, headers, timeout, conn)
    else:
        return await _download_image(url, save_path, headers, timeout, conn)

async def _download_image(url, save_path, headers, timeout, conn):
    try:
        async with aiohttp.ClientSession(headers=headers, timeout=timeout, connector=conn) as sess:
            async with sess.get(url=url) as response:
                if response.status == 200:
                    ensure_dir(os.path.dirname(save_path))
                    async with aiofiles.open(save_path, mode="wb") as f:
                        await f.write(await response.content.read())
                    return True
                else:
                    # 尝试切换图片格式
                    if url[-3:] == 'png':
                        url = url[:-3] + 'jpg'
                    elif url[-3:] == 'jpg':
                        url = url[:-3] + 'png'
                    async with sess.get(url=url) as response:
                        if response.status == 200:
                            ensure_dir(os.path.dirname(save_path))
                            async with aiofiles.open(save_path, mode="wb") as f:
                                await f.write(await response.content.read())
                            return True
                        return False
    except Exception as e:
        print(f"下载失败: {url}, 错误: {str(e)}")
        return False

# 检查图片是否为空
def is_image_empty(image_path):
    try:
        im = np.fromfile(image_path, dtype=np.uint8)
        return len(im) == 0
    except:
        return True

# 压缩目录
def zip_directory(dirpath, out_full_name):
    print('正在压缩文件...')
    with zipfile.ZipFile(out_full_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for path, dirnames, filenames in os.walk(dirpath):
            fpath = path.replace(dirpath, '')
            for filename in filenames:
                zipf.write(os.path.join(path, filename), os.path.join(fpath, filename))
    print('压缩完成')

# 删除目录
def delete_directory(rootdir):
    print('正在删除原文件...')
    if os.path.exists(rootdir):
        shutil.rmtree(rootdir, True)
    print('删除完成')
