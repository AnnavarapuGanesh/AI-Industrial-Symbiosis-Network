import asyncio
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import engine, Base, get_db
import models
import schemas
from vector_db import init_db
from workflow import orchestrator

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WasteLink AI MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/industries")
def get_industries():
    # Return static nodes for map plotting
    return list(orchestrator.industries.values())

@app.post("/api/submit-waste")
async def submit_waste(event: schemas.WasteEvent):
    try:
        await orchestrator.process_waste_event(event.producer_id, event.raw_text)
        return {"status": "success"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

@app.post("/api/reset")
def reset_demo(db: Session = Depends(get_db)):
    db.query(models.MatchRecord).delete()
    db.commit()
    
    # Ping WS to clear UI
    asyncio.create_task(orchestrator.message_queue.put({"agent": "System", "message": "RESET_DEMO"}))
    return {"status": "cleared"}

@app.websocket("/ws/feed")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # We poll from the central queue and send to client
            # Note: In a real multi-client app, each connection needs its own queue listener.
            # For a hackathon MVP with 1 dashboard, sharing the global queue works perfectly.
            msg = await orchestrator.message_queue.get()
            await websocket.send_text(json.dumps(msg))
    except WebSocketDisconnect:
        pass
