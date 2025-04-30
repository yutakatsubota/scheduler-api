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

# 共通アーカイブ関数
def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=HEADERS, json={"archived": True})
    print("DEBUG ARCHIVE PAGE:", response.status_code, response.text)
    return response.status_code

# 共通FETCH関数
def fetch_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS)
    print("DEBUG FETCH DATABASE:", response.status_code, response.text)  # デバッグログ
    return response.status_code, response.json()


# 1. 一ヶ月の目標（monthly_goal）
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

def update_monthly_goal(page_id, data):
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
    print("DEBUG PATCH MONTHLY GOAL:", response.status_code, response.text)
    return response.status_code

def delete_from_monthly_goal(page_id):
    return archive_page(page_id)

def fetch_monthly_goal():
    return fetch_database(DB_ID_MONTHLY_GOAL)


# 2. 三日の目標（3day_goal）
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

def update_3day_goal(page_id, data):
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
    print("DEBUG PATCH 3DAY GOAL:", response.status_code, response.text)
    return response.status_code

def delete_from_3day_goal(page_id):
    return archive_page(page_id)

def fetch_3day_goal():
    return fetch_database(DB_ID_3DAY_GOAL)


# 3. 一日のスケジュール（schedule）
def write_to_schedule(data):
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

def update_schedule(page_id, data):
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

def delete_schedule(page_id):
    return archive_page(page_id)

def fetch_schedule():
    return fetch_database(DATABASE_ID)


# 4. Tストック（t_stock）
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

def update_t_stock(page_id, data):
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
    print("DEBUG PATCH T_STOCK:", response.status_code, response.text)
    return response.status_code

def delete_from_t_stock(page_id):
    return archive_page(page_id)

def fetch_t_stock():
    return fetch_database(DB_ID_T_STOCK)


# 5. 運用DB（operation_db）
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

def fetch_operation_db():
    return fetch_database(DB_ID_OPERATION)


# 6. 改善アイディアDB（idea_db）
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

def fetch_idea_db():
    return fetch_database(DB_ID_IDEA)