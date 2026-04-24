# Comic Spider

多网站漫画爬虫工具，支持多个漫画网站的漫画下载。

## 支持的网站

- **copy_comic**: https://www.copymanga.org
- **zones_comic**: http://www.zerobywgeat.com
- **dmhuah**: https://m.dmhuah.com

## 功能特性

- 支持多个漫画网站
- 异步下载，提高下载速度
- 自动处理图片格式转换
- 支持搜索漫画
- 支持章节范围下载
- 支持打包成压缩包
- 错误处理和重试机制

## 安装

### 方法一：使用pip安装

```bash
pip install -e .
```

### 方法二：直接运行

1. 克隆项目
2. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 列出支持的网站

```bash
comic-spider list-sites
```

### 下载漫画

#### 方法一：通过URL下载

```bash
comic-spider download --site copy_comic --url https://www.copymanga.org/comic/daerwenyouxi --comic-name "达尔文游戏"
```

#### 方法二：通过关键词搜索下载

```bash
comic-spider download --site zones_comic --keyword "海贼王" --comic-name "海贼王"
```

### 高级选项

- `--start-chapter`: 开始章节索引（默认0）
- `--end-chapter`: 结束章节索引（默认-1，即全部）
- `--zip`: 下载完成后打包成压缩包

示例：下载前10章并打包

```bash
comic-spider download --site copy_comic --url https://www.copymanga.org/comic/daerwenyouxi --comic-name "达尔文游戏" --start-chapter 0 --end-chapter 10 --zip
```

## 配置

配置文件位于 `comic_spider/config/config.py`，可以修改以下配置：

- `BASE_DOWNLOAD_PATH`: 下载路径（默认：用户Downloads目录下的comic文件夹）
- `CONCURRENT_LIMIT`: 并发下载限制（默认：80）
- `HEADLESS`: 是否使用无头浏览器（默认：True）
- `CHROME_DRIVER_PATH`: Chrome驱动路径（默认：自动查找）
- `HEADERS`: 请求头
- `TIMEOUT`: 超时时间（默认：30秒）
- `RETRY_COUNT`: 重试次数（默认：3）

## 依赖

- requests
- lxml
- selenium
- aiohttp
- aiofiles
- numpy
- click

## 注意事项

1. 请遵守网站的爬虫规则，不要过度请求
2. 部分网站可能需要登录才能访问完整内容
3. 本工具仅用于个人学习和研究，请勿用于商业用途

## 许可证

MIT License
