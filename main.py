from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
import os
print("NOTION_TOKEN:", os.getenv("NOTION_TOKEN"))

from fastapi import FastAPI, Request
from notion_writer import (
    write_to_notion,
    write_to_t_stock,
    write_to_3day_goal,
    write_to_monthly_goal,
    delete_from_t_stock,
    delete_from_3day_goal,
    delete_from_monthly_goal,
    update_page_in_db,
    update_schedule_in_db,
    archive_page,   # ←これ追加！

    write_to_operation_db,
    update_operation_db,
    delete_from_operation_db,
    write_to_idea_db,
    update_idea_db,
    delete_from_idea_db,
    fetch_operation_db,
    fetch_idea_db
)
import uvicorn

app = FastAPI()

@app.post("/schedule")
async def add_schedule(req: Request):
    data = await req.json()
    result = write_to_notion(data)
    return {"status": "ok", "result": result}

@app.post("/t_stock")
async def post_to_t_stock(request: Request):
    data = await request.json()
    result = write_to_t_stock(data)
    return {"status": "ok", "result": result}

@app.post("/3day_goal")
async def post_to_3day_goal(request: Request):
    data = await request.json()
    result = write_to_3day_goal(data)
    return {"status": "ok", "result": result}

@app.post("/monthly_goal")
async def post_to_monthly_goal(request: Request):
    data = await request.json()
    result = write_to_monthly_goal(data)
    return {"status": "ok", "result": result}

@app.delete("/t_stock/{page_id}")
async def delete_t_stock(page_id: str):
    result = delete_from_t_stock(page_id)
    return {"status": "ok", "result": result}

@app.delete("/3day_goal/{page_id}")
async def delete_3day_goal(page_id: str):
    result = delete_from_3day_goal(page_id)
    return {"status": "ok", "result": result}

@app.delete("/monthly_goal/{page_id}")
async def delete_monthly_goal(page_id: str):
    result = delete_from_monthly_goal(page_id)
    return {"status": "ok", "result": result}

@app.delete("/schedule/{page_id}")
async def delete_schedule(page_id: str):
    result = archive_page(page_id)
    return {"status": "ok", "result": result}

@app.patch("/t_stock/{page_id}")
async def update_t_stock(page_id: str, request: Request):
    data = await request.json()
    result = update_page_in_db(page_id, data)
    return {"status": "ok", "result": result}

@app.patch("/3day_goal/{page_id}")
async def update_3day_goal(page_id: str, request: Request):
    data = await request.json()
    result = update_page_in_db(page_id, data)
    return {"status": "ok", "result": result}

@app.patch("/monthly_goal/{page_id}")
async def update_monthly_goal(page_id: str, request: Request):
    data = await request.json()
    result = update_page_in_db(page_id, data)
    return {"status": "ok", "result": result}

@app.post("/operation_db")
async def post_to_operation_db(request: Request):
    data = await request.json()
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

@app.post("/idea_db")
async def post_to_idea_db(request: Request):
    data = await request.json()
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

@app.patch("/schedule/{page_id}")
async def update_schedule(page_id: str, request: Request):
    data = await request.json()
    result = update_schedule_in_db(page_id, data)
    return {"status": "ok", "result": result}


# New endpoints for /fetch/operation_db and /fetch/idea_db
@app.get("/fetch/operation_db")
async def fetch_operation_db_endpoint():
    status_code, result = fetch_operation_db()
    return {"status": status_code, "result": result}

@app.get("/fetch/idea_db")
async def fetch_idea_db_endpoint():
    status_code, result = fetch_idea_db()
    return {"status": status_code, "result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)