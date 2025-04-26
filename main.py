import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from notion_writer import (
    write_to_notion,
    write_to_t_stock,
    write_to_3day_goal,
    write_to_monthly_goal,
    delete_from_t_stock,
    delete_from_3day_goal,
    delete_from_monthly_goal,
    update_page_in_db
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
