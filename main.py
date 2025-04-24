from fastapi import FastAPI, Request
from notion_writer import write_to_notion
import uvicorn

app = FastAPI()

@app.post("/schedule")
async def add_schedule(req: Request):
    data = await req.json()
    result = write_to_notion(data)
    return {"status": "ok", "result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)