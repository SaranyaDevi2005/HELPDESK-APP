from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from models import Ticket, TicketUpdate
from database import tickets_col, users_col
from bson import ObjectId
from email_utils import send_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── TICKETS ───────────────────────────────────────

@app.post("/tickets")
def create_ticket(ticket: Ticket, background_tasks: BackgroundTasks):
    print("🔥 Creating ticket for:", ticket.created_by)

    result = tickets_col.insert_one(ticket.dict())

    user = users_col.find_one({"username": ticket.created_by})

    if user and "email" in user:
        background_tasks.add_task(
            send_email,
            user["email"],
            "🎫 Ticket Created",
            f"""
            Hello {user['username']},

            Your ticket "{ticket.title}" has been successfully created.

            We will update you soon.

            - HelpDesk Team
            """
        )

    return {"id": str(result.inserted_id), "message": "Ticket created"}


@app.get("/tickets")
def get_all_tickets():
    tickets = []
    for t in tickets_col.find():
        t["_id"] = str(t["_id"])
        tickets.append(t)
    return tickets


@app.get("/tickets/{username}")
def get_user_tickets(username: str):
    tickets = []
    for t in tickets_col.find({"created_by": username}):
        t["_id"] = str(t["_id"])
        tickets.append(t)
    return tickets


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, update: TicketUpdate, background_tasks: BackgroundTasks):

    print("🔥 Update request:", update.dict())

    ticket = tickets_col.find_one({"_id": ObjectId(ticket_id)})

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    old_status = ticket.get("status")

    tickets_col.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": update.dict(exclude_none=True)}
    )

    new_status = update.status if update.status else old_status

    user = users_col.find_one({"username": ticket["created_by"]})

    print("👤 User found:", user)

    if user and "email" in user and update.status:

        print("📨 Triggering email...")

        background_tasks.add_task(
            send_email,
            user["email"],
            "🔄 Ticket Status Updated",
            f"""
Hello {user['username']},

Your ticket "{ticket['title']}" has been updated.

Old Status: {old_status}
New Status: {new_status}

- HelpDesk Team
"""
        )

    return {"message": "Ticket updated"}


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):
    tickets_col.delete_one({"_id": ObjectId(ticket_id)})
    return {"message": "Ticket deleted"}


# ── STATS ─────────────────────────────────────────

@app.get("/stats")
def get_stats():
    total = tickets_col.count_documents({})
    open_ = tickets_col.count_documents({"status": "Open"})
    in_progress = tickets_col.count_documents({"status": "In Progress"})
    resolved = tickets_col.count_documents({"status": "Resolved"})
    high_priority = tickets_col.count_documents({"priority": "High"})

    return {
        "total": total,
        "open": open_,
        "in_progress": in_progress,
        "resolved": resolved,
        "high_priority": high_priority
    }


@app.get("/health")
def health():
    return {"status": "ok"}