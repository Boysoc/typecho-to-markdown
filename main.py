import pymysql
import os
import re
from datetime import datetime
from pypinyin import lazy_pinyin

def to_isoformat_z(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def make_slug(title):
    slug = ''.join(lazy_pinyin(title))
    slug = slug.lower()
    slug = re.sub(r'\s+', '_', slug)
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    return slug if slug else "post"

def clean_text(text):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'!\[.*?\]\[.*?\]', '', text)
    text = re.sub(r'\[.*?\]:\s*.*', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'\n', '', text)
    return text

def chinese_excerpt(text, length=30):
    zh = ''.join(re.findall(r'[\u4e00-\u9fff，。！？,.!?a-zA-Z0-9]', text))
    return zh[:length]

def extract_tags(text):
    keyword_list = ["感悟", "成长", "随笔", "人生", "思考", "回忆", "梦想", "情感", "抒情","旅行", "失眠", "学车",  "手表", "生活", "足彩", "分享", "记录"]
    tags = []
    for word in keyword_list:
        if word in text and word not in tags:
            tags.append(word)
    if not tags:
        tags.append("随笔")
    return tags

def fix_md_images(text):
    # 处理 [编号]: url 行，处理 ![xxx][编号] -> ![xxx](url)
    ref_map = dict(re.findall(r'^\s*\[(\d+)\]:\s*(\S+)', text, flags=re.MULTILINE))
    def replace_img(m):
        alt = m.group(1)
        idx = m.group(2)
        url = ref_map.get(idx, '')
        return f'![{alt}]({url})' if url else m.group(0)
    text = re.sub(r'!\[([^\]]+)\]\[(\d+)\]', replace_img, text)
    text = re.sub(r'^\s*\[(\d+)\]:\s*\S+\s*$', '', text, flags=re.MULTILINE)
    def html_img_to_md(match):
        attrs = match.group(1)
        src = re.search(r'src=["\'](.*?)["\']', attrs, flags=re.IGNORECASE)
        alt = re.search(r'alt=["\'](.*?)["\']', attrs, flags=re.IGNORECASE)
        url = src.group(1) if src else ''
        desc = alt.group(1) if alt else ''
        return f'![{desc}]({url})' if url else ''
    text = re.sub(r'<img\s+(.*?)\s*/?>', html_img_to_md, text, flags=re.IGNORECASE)
    def remove_outer_tag(tag, text):
        return re.sub(fr'<{tag}[^>]*>(.*?)</{tag}>', lambda m: m.group(1).strip(), text, flags=re.IGNORECASE|re.DOTALL)
    for tag in ['p', 'span', 'div']:
        text = remove_outer_tag(tag, text)
    text = re.sub(r'style\s*=\s*"[^"]*"', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text

def remove_markdown_comment(text):
    return re.sub(r'<!--\s*markdown\s*-->', '', text, flags=re.IGNORECASE)

def escape(s):
    return str(s).replace('\n', ' ').replace('\r', '')

def main():
    MYSQL_CONFIG = {
        'host': '主机',
        'user': '用户名',
        'password': '密码',
        'database': '数据库',
        'charset': 'utf8'
    }

    db = pymysql.connect(**MYSQL_CONFIG)
    print("连接成功")
    cur = db.cursor()

    cur.execute("SELECT cid, title, created, text FROM typecho_contents WHERE type='post'")
    posts = cur.fetchall()

    os.makedirs("export", exist_ok=True)

    for cid, title, created, text in posts:
        print(f"处理 ------>  {title}")
        pubDatetime = to_isoformat_z(created)
        filename = f"{datetime.fromtimestamp(created).strftime('%Y-%m-%d')}.md"
        slug = make_slug(title)

        clean = clean_text(text)
        description = escape(chinese_excerpt(clean, 30))
        excerpt = escape(chinese_excerpt(clean, 100))
        tags = extract_tags(clean)
        tags_fmt = "[" + ", ".join([f'{t}' for t in tags]) + "]"

        body = remove_markdown_comment(text)
        body = fix_md_images(body).strip()

        front_matter = f"""---
pubDatetime: {pubDatetime}
title: {escape(title)}
slug: {slug}
description: {description}
tags: {tags_fmt}
featured: false
draft: false
excerpt: {excerpt}
---

{body}
"""

        with open(f"export/{filename}", "w", encoding="utf-8") as f:
            f.write(front_matter)
        # 可选：输出导出进度
        # print(f"导出: export/{filename}")

    cur.close()
    db.close()

if __name__ == "__main__":
    main()
