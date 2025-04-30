# notion_writer.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
DB_ID_T_STOCK = os.getenv("DB_ID_T_STOCK")
DB_ID_3DAY_GOAL = os.getenv("DB_ID_3DAY_GOAL")
DB_ID_MONTHLY_GOAL = os.getenv("DB_ID_MONTHLY_GOAL")
DB_ID_OPERATION = os.getenv("DB_ID_OPERATION")
DB_ID_IDEA = os.getenv("DB_ID_IDEA")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


# スケジュールログ用
def write_to_notion(data):
    url = "https://api.notion.com/v1/pages"
    properties = {
        "日付": {"date": {"start": data["date"]}},
        "内容": {"title": [{"text": {"content": data["content"]}}]},
        "目安時間": {"rich_text": [{"text": {"content": data["duration"]}}]},
        "カテゴリ": {"select": {"name": data["category"]}},
        **({"実行状況": {"select": {"name": data["status"]}}} if "status" in data and data["status"] else {}),
        **({"振り返り": {"rich_text": [{"text": {"content": data["review"]}}]}} if "review" in data and data["review"] else {})
    }
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST SCHEDULE:", response.status_code, response.text)
    return response.status_code

def update_schedule_in_db(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    properties = {}
    if "date" in data and data["date"]:
        properties["日付"] = {"date": {"start": data["date"]}}
    if "content" in data and data["content"]:
        properties["内容"] = {"title": [{"text": {"content": data["content"]}}]}
    if "duration" in data and data["duration"]:
        properties["目安時間"] = {"rich_text": [{"text": {"content": data["duration"]}}]}
    if "category" in data and data["category"]:
        properties["カテゴリ"] = {"select": {"name": data["category"]}}
    if "status" in data and data["status"]:
        properties["実行状況"] = {"select": {"name": data["status"]}}
    if "review" in data and data["review"]:
        properties["振り返り"] = {"rich_text": [{"text": {"content": data["review"]}}]}
    if not properties:
        print("DEBUG PATCH SKIPPED: empty properties")
        return 400
    payload = {
        "properties": properties
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    print("DEBUG PATCH SCHEDULE:", response.status_code, response.text)
    return response.status_code

# 共通アーカイブ関数
def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=HEADERS, json={"archived": True})
    print("DEBUG ARCHIVE PAGE:", response.status_code, response.text)
    return response.status_code

# Tストック／3日目標／1ヶ月目標用
def write_to_t_stock(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID_T_STOCK},
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"title": [{"text": {"content": data["content"]}}]}
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST T_STOCK:", response.status_code, response.text)
    return response.status_code

def write_to_3day_goal(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID_3DAY_GOAL},
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"title": [{"text": {"content": data["content"]}}]},
            **({"振り返り": {"rich_text": [{"text": {"content": data["review"]}}]}} if "review" in data and data["review"] else {})
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST 3DAY GOAL:", response.status_code, response.text)
    return response.status_code

def write_to_monthly_goal(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID_MONTHLY_GOAL},
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"title": [{"text": {"content": data["content"]}}]},
            **({"振り返り": {"rich_text": [{"text": {"content": data["review"]}}]}} if "review" in data and data["review"] else {})
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST MONTHLY GOAL:", response.status_code, response.text)
    return response.status_code

# 共通PATCH用（Tストック、3日目標、1ヶ月目標）
def update_page_in_db(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    properties = {}
    if "date" in data:
        properties["日付"] = {"date": {"start": data["date"]}}
    if "content" in data:
        properties["内容"] = {"title": [{"text": {"content": data["content"]}}]}
    if "review" in data and data["review"]:
        properties["振り返り"] = {"rich_text": [{"text": {"content": data["review"]}}]}
    if not properties:
        print("DEBUG PATCH SKIPPED: empty properties")
        return 400
    payload = {
        "properties": properties
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    print("DEBUG PATCH PAGE:", response.status_code, response.text)
    return response.status_code

# Tストック／3日目標／1ヶ月目標用アーカイブ
def delete_from_t_stock(page_id):
    return archive_page(page_id)

def delete_from_3day_goal(page_id):
    return archive_page(page_id)

def delete_from_monthly_goal(page_id):
    return archive_page(page_id)

# 運用DB (operation_db) 用関数
def write_to_operation_db(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID_OPERATION},
        "properties": {
            "タイトル": {"title": [{"text": {"content": data["title"]}}]},
            "内容": {"rich_text": [{"text": {"content": data["content"]}}]}
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST OPERATION DB:", response.status_code, response.text)
    return response.status_code

def update_operation_db(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    properties = {}
    if "title" in data:
        properties["タイトル"] = {"title": [{"text": {"content": data["title"]}}]}
    if "content" in data:
        properties["内容"] = {"rich_text": [{"text": {"content": data["content"]}}]}
    if not properties:
        print("DEBUG PATCH SKIPPED: empty properties")
        return 400
    payload = {
        "properties": properties
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    print("DEBUG PATCH OPERATION DB:", response.status_code, response.text)
    return response.status_code

def delete_from_operation_db(page_id):
    return archive_page(page_id)

# 改善アイディアDB (idea_db) 用関数
def write_to_idea_db(data):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID_IDEA},
        "properties": {
            "日付": {"date": {"start": data["date"]}},
            "内容": {"rich_text": [{"text": {"content": data["content"]}}]}
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("DEBUG POST IDEA DB:", response.status_code, response.text)
    return response.status_code

def update_idea_db(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    properties = {}
    if "date" in data:
        properties["日付"] = {"date": {"start": data["date"]}}
    if "content" in data:
        properties["内容"] = {"title": [{"text": {"content": data["content"]}}]}
    if not properties:
        print("DEBUG PATCH SKIPPED: empty properties")
        return 400
    payload = {
        "properties": properties
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    print("DEBUG PATCH IDEA DB:", response.status_code, response.text)
    return response.status_code

def delete_from_idea_db(page_id):
    return archive_page(page_id)

def fetch_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS)
    print("DEBUG FETCH DATABASE:", response.status_code, response.text)  # デバッグログ
    return response.status_code, response.json()
def fetch_operation_db():
    url = f"https://api.notion.com/v1/databases/{DB_ID_OPERATION}/query"
    response = requests.post(url, headers=HEADERS)
    print("DEBUG FETCH OPERATION DB:", response.status_code, response.text)
    return response.status_code, response.json()

def fetch_idea_db():
    url = f"https://api.notion.com/v1/databases/{DB_ID_IDEA}/query"
    response = requests.post(url, headers=HEADERS)
    print("DEBUG FETCH IDEA DB:", response.status_code, response.text)
    return response.status_code, response.json()