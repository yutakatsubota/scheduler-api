# notion_writer.py

import os
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

def write_to_notion(data):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    url = f"https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"title": [{"text": {"content": data["content"]}}]},
            "カテゴリ": {"select": {"name": data["category"]}},
            "目安時間": {"rich_text": [{"text": {"content": data["duration"]}}]}
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code