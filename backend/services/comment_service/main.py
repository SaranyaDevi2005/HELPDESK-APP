from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Comment
from database import comments_col
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── COMMENTS ──────────────────────────────────────

@app.post("/tickets/{ticket_id}/comments")
def add_comment(ticket_id: str, comment: Comment):
    data = comment.dict()
    data["created_at"] = datetime.utcnow().isoformat()
    comments_col.insert_one(data)
    return {"message": "Comment added"}


@app.get("/tickets/{ticket_id}/comments")
def get_comments(ticket_id: str):
    result = []
    for c in comments_col.find({"ticket_id": ticket_id}):
        c["_id"] = str(c["_id"])
        result.append(c)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}