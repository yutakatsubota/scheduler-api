# notion_writer.py

import os
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
def write_to_notion(data):
    url = "https://api.notion.com/v1/pages"

    properties = {
        "日付": {"date": {"start": data["date"]}},
        "内容": {"title": [{"text": {"content": data["content"]}}]},
        "目安時間": {"rich_text": [{"text": {"content": data["duration"]}}]},
        "カテゴリ": {"rich_text": [{"text": {"content": data["category"]}}]},
        "実行状況": {"select": {"name": data["status"]}},
        "振り返り": {"rich_text": [{"text": {"content": data["review"]}}]}
    }

    payload = {
        "parent": {"database_id": os.getenv("DATABASE_ID")},
        "properties": properties
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST:", response.status_code, response.text)
    return response.status_code

def write_to_t_stock(data):
    return write_to_notion_with_db_id(data, os.getenv("DB_ID_T_STOCK"))

def write_to_3day_goal(data):
    return write_to_notion_with_db_id(data, os.getenv("DB_ID_3DAY_GOAL"))

def write_to_monthly_goal(data):
    return write_to_notion_with_db_id(data, os.getenv("DB_ID_MONTHLY_GOAL"))

def write_to_notion_with_db_id(data, db_id):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"title": [{"text": {"content": data["content"]}}]}
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG:", response.status_code, response.text)  # レスポンスの詳細を出力する行を追加
    return response.status_code

def delete_from_t_stock(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "archived": True
    }
    response = requests.patch(url, headers=headers, json=payload)
    print("DEBUG DELETE:", response.status_code, response.text)  # ここでレスポンス詳細を出力
    return response.status_code

def delete_from_3day_goal(page_id):
    return archive_page(page_id)

def delete_from_monthly_goal(page_id):
    return archive_page(page_id)

def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=HEADERS, json={"archived": True})
    print("DEBUG DELETE:", response.status_code, response.text)
    return response.status_code

def update_page_in_db(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"title": [{"text": {"content": data["content"]}}]}
        }
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    print("DEBUG PATCH:", response.status_code, response.text)
    return response.status_code