import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from notion_writer import write_to_notion

from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/schedule")
async def add_schedule(req: Request):
    data = await req.json()
    result = write_to_notion(data)
    return {"status": "ok", "result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

    from fastapi import FastAPI, Request
from notion_writer import write_to_t_stock, write_to_3day_goal, write_to_monthly_goal

app = FastAPI()

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

