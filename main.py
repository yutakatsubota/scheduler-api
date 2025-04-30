from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
import os
print("NOTION_TOKEN:", os.getenv("NOTION_TOKEN"))

from fastapi import FastAPI, Request
from notion_writer import (
    # monthly_goal
    write_to_monthly_goal,
    update_monthly_goal,
    delete_from_monthly_goal,
    fetch_monthly_goal,
    # 3day_goal
    write_to_3day_goal,
    update_3day_goal,
    delete_from_3day_goal,
    fetch_3day_goal,
    # schedule
    write_to_schedule,
    update_schedule,
    archive_page,
    fetch_schedule,
    # t_stock
    write_to_t_stock,
    update_t_stock,
    delete_from_t_stock,
    fetch_t_stock,
    # operation_db
    write_to_operation_db,
    update_operation_db,
    delete_from_operation_db,
    fetch_operation_db,
    # idea_db
    write_to_idea_db,
    update_idea_db,
    delete_from_idea_db,
    fetch_idea_db
)
import uvicorn

app = FastAPI()

# 1. 一ヶ月の目標
@app.post("/monthly_goal")
async def post_to_monthly_goal(request: Request):
    data = await request.json()
    print("DEBUG POST monthly_goal:", data)
    data["review"] = data.get("review", "")
    result = write_to_monthly_goal(data)
    return {"status": "ok", "result": result}

@app.patch("/monthly_goal/{page_id}")
async def patch_monthly_goal(page_id: str, request: Request):
    data = await request.json()
    result = update_monthly_goal(page_id, data)
    return {"status": "ok", "result": result}

@app.delete("/monthly_goal/{page_id}")
async def delete_monthly_goal(page_id: str):
    result = delete_from_monthly_goal(page_id)
    return {"status": "ok", "result": result}

@app.get("/monthly_goal")
async def get_monthly_goal():
    status_code, result = fetch_monthly_goal()
    return {"status": status_code, "result": result}

# 2. 三日の目標
@app.post("/3day_goal")
async def post_to_3day_goal(request: Request):
    data = await request.json()
    data["review"] = data.get("review", "")
    result = write_to_3day_goal(data)
    return {"status": "ok", "result": result}

@app.patch("/3day_goal/{page_id}")
async def patch_3day_goal(page_id: str, request: Request):
    data = await request.json()
    result = update_3day_goal(page_id, data)
    return {"status": "ok", "result": result}

@app.delete("/3day_goal/{page_id}")
async def delete_3day_goal(page_id: str):
    result = delete_from_3day_goal(page_id)
    return {"status": "ok", "result": result}

@app.get("/3day_goal")
async def get_3day_goal():
    status_code, result = fetch_3day_goal()
    return {"status": status_code, "result": result}

# 3. 一日のスケジュール
@app.post("/schedule")
async def post_to_schedule(req: Request):
    data = await req.json()
    data["status"] = data.get("status", "")
    data["review"] = data.get("review", "")
    result = write_to_schedule(data)
    return {"status": "ok", "result": result}

@app.patch("/schedule/{page_id}")
async def patch_schedule(page_id: str, request: Request):
    data = await request.json()
    result = update_schedule(page_id, data)
    return {"status": "ok", "result": result}

@app.delete("/schedule/{page_id}")
async def delete_schedule(page_id: str):
    result = archive_page(page_id)
    return {"status": "ok", "result": result}

@app.get("/schedule")
async def get_schedule():
    status_code, result = fetch_schedule()
    return {"status": status_code, "result": result}

# 4. Tストック
@app.post("/t_stock")
async def post_to_t_stock(request: Request):
    data = await request.json()
    data["memo"] = data.get("memo", "")
    result = write_to_t_stock(data)
    return {"status": "ok", "result": result}

@app.patch("/t_stock/{page_id}")
async def patch_t_stock(page_id: str, request: Request):
    data = await request.json()
    result = update_t_stock(page_id, data)
    return {"status": "ok", "result": result}

@app.delete("/t_stock/{page_id}")
async def delete_t_stock(page_id: str):
    result = delete_from_t_stock(page_id)
    return {"status": "ok", "result": result}

@app.get("/t_stock")
async def get_t_stock():
    status_code, result = fetch_t_stock()
    return {"status": status_code, "result": result}

# 5. 運用DB
@app.post("/operation_db")
async def post_to_operation_db(request: Request):
    data = await request.json()
    data["memo"] = data.get("memo", "")
    result = write_to_operation_db(data)
    return {"status": "ok", "result": result}

@app.patch("/operation_db/{page_id}")
async def patch_operation_db(page_id: str, request: Request):
    data = await request.json()
    result = update_operation_db(page_id, data)
    return {"status": "ok", "result": result}

@app.delete("/operation_db/{page_id}")
async def delete_operation_db(page_id: str):
    result = delete_from_operation_db(page_id)
    return {"status": "ok", "result": result}

@app.get("/operation_db")
async def get_operation_db():
    status_code, result = fetch_operation_db()
    return {"status": status_code, "result": result}

# 6. 改善アイディア
@app.post("/idea_db")
async def post_to_idea_db(request: Request):
    data = await request.json()
    data["memo"] = data.get("memo", "")
    result = write_to_idea_db(data)
    return {"status": "ok", "result": result}

@app.patch("/idea_db/{page_id}")
async def patch_idea_db(page_id: str, request: Request):
    data = await request.json()
    result = update_idea_db(page_id, data)
    return {"status": "ok", "result": result}

@app.delete("/idea_db/{page_id}")
async def delete_idea_db(page_id: str):
    result = delete_from_idea_db(page_id)
    return {"status": "ok", "result": result}

@app.get("/idea_db")
async def get_idea_db():
    status_code, result = fetch_idea_db()
    return {"status": status_code, "result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)