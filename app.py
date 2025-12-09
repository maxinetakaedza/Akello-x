from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from datastore import DataStore
from rules_engine import RuleEngine

# create app and services
app = FastAPI(title="Rule-Based Student Decision Engine (prototype)")

ds = DataStore()
engine = RuleEngine(ds)

# load a sample question bank (could be replaced with repo bank)
sample_questions = [
    {"id": "q1", "topic": "algebra/linear-equations", "difficulty": "easy", "type": "mcq"},
    {"id": "q2", "topic": "algebra/linear-equations", "difficulty": "medium", "type": "short_answer"},
    {"id": "q3", "topic": "algebra/inequalities", "difficulty": "hard", "type": "problem"},
    {"id": "q4", "topic": "algebra/inequalities", "difficulty": "easy", "type": "mcq"}
]
ds.add_question_bank(sample_questions)

class AttemptIn(BaseModel):
    student_id: str
    question_id: str
    topic: str
    difficulty: str
    correct: bool
    time_spent_seconds: Optional[int] = None
    # optional: tags, subtopic, attempts_count
    tags: Optional[List[str]] = []

@app.post("/attempt")
def submit_attempt(a: AttemptIn):
    if a.question_id not in ds.questions:
        # not fatal; allow unknown question (bank might be external)
        pass
    attempt = a.dict()
    decision = engine.process_attempt(a.student_id, attempt)
    return decision

@app.get("/profile/{student_id}")
def get_profile(student_id: str):
    return ds.get_profile(student_id)

@app.get("/induce_rules")
def induce_rules(student_ids: Optional[str] = None):
    sids = student_ids.split(",") if student_ids else None
    proposals = engine.induce_candidate_rules(sids)
    return {"candidate_rules": proposals}

# If running as script
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
