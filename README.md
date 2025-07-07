# Typecho Markdown 导出脚本

本项目是一个将 [Typecho](https://typecho.org/) 博客系统文章**批量导出为 Markdown 文件**的小工具，自动处理图片与 YAML 头信息，适合备份、迁移到 Astro、Hexo、Hugo、Jekyll 等静态博客。

> **作者：[Boysoc](https://github.com/boysoc)**  
> 欢迎 Star、PR 与建议！

---

## ✨ 项目特点

- 直接从 Typecho MySQL 数据库读取文章内容
- 每篇文章导出为单独的 Markdown 文件，自动生成 YAML Front-matter
- 文章标题自动转为拼音 slug
- 智能提取摘要（excerpt）与标签（tags），Front-matter 美观规范
- 图片 HTML 自动转换为 Markdown 语法，清理无用 HTML 与注释
- 完美中文环境支持，简洁易用

---

## 🚀 快速开始

### 1. 环境要求

- Python ≥ 3.7

### 2. 安装依赖

```bash
pip install pymysql pypinyin
```
### 3. 配置数据库
编辑 main.py，填入你的 Typecho 数据库信息：
```bash
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '你的密码',
    'database': '你的数据库名',
    'charset': 'utf8'
}
```
### 4. 运行脚本
```bash
python main.py
```
运行后，会在 export/ 目录下生成所有博客文章的 Markdown 文件，文件名为日期格式（如 2021-08-21.md）。

##📂目录结构示例
```bash
your_project/
├─ main.py
├─ export/
│   ├─ 2021-08-21.md
│   ├─ 2021-08-23.md
│   └─ ...
└─ README.md
```
##🦄 适用场景
Typecho 博客迁移到 Astro / Hexo / Hugo / Jekyll 等静态博客系统
本地归档、内容备份
用 Github/Gitee 托管自己的博客内容


##⚠️ 注意事项
默认导出所有普通博文（type='post'），如有特殊需求可调整 SQL
Front-matter 可按需扩展、重命名
本项目仅用于个人数据迁移与备份，涉及数据安全请务必谨慎

##🙌 欢迎 PR & 建议！
一键导出 Typecho 文章为带 front-matter 的 Markdown 文件，方便静态博客迁移与内容备份。

---
