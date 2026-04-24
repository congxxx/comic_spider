# 推送到GitHub的步骤

## 前提条件

1. 已安装Git
2. 已在GitHub上创建了一个新的仓库
3. 已完成项目的开发和测试

## 步骤

### 1. 初始化Git仓库

在项目根目录执行：

```bash
git init
```

### 2. 添加文件到暂存区

```bash
git add .
```

### 3. 提交代码

```bash
git commit -m "Initial commit: 多网站漫画爬虫工具"
```

### 4. 关联远程仓库

```bash
git remote add origin https://github.com/yourusername/comic_spider.git
```

### 5. 推送到GitHub

```bash
git push -u origin main
```

## 注意事项

1. 请将 `yourusername` 替换为你的GitHub用户名
2. 请确保 `.gitignore` 文件已正确配置，避免将不必要的文件推送到GitHub
3. 首次推送时可能需要输入GitHub的用户名和密码或个人访问令牌
4. 如果远程仓库已存在且有内容，可能需要先拉取并解决冲突

## 后续维护

1. 定期更新代码并提交
2. 修复bug和添加新功能
3. 更新README.md文件，保持文档的准确性
4. 考虑添加CI/CD流程，自动测试和部署

## 分支管理

建议使用以下分支策略：
- `main`: 主分支，存放稳定版本
- `develop`: 开发分支，用于集成新功能
- `feature/*`: 特性分支，用于开发具体功能
- `bugfix/*`: 修复分支，用于修复bug
