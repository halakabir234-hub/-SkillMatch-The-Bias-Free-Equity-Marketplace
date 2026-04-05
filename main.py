from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is where your 'Postings' will live!
# It starts with one fake person so the board isn't empty.
talent_pool = [
    {"id": "PRO-1", "name": "Sarah Ahmed", "skills": "Python, FastAPI", "whatsapp": "923001234567"}
]

class TalentEntry(BaseModel):
    name: str
    skills: str
    whatsapp: str

@app.post("/login")
def login(user: TalentEntry):
    return {"status": "Logged In", "user": user.name}

@app.post("/post-to-board")
def post_talent(entry: TalentEntry):
    new_id = f"DEV-{len(talent_pool) + 1}"
    new_entry = {
        "id": new_id,
        "name": entry.name,
        "skills": entry.skills,
        "whatsapp": entry.whatsapp
    }
    talent_pool.append(new_entry)
    return {"status": "Posted Successfully", "id": new_id}

@app.get("/search")
def search(skills: str = ""):
    if not skills:
        return talent_pool
    results = [p for p in talent_pool if skills.lower() in p["skills"].lower()]
    return results