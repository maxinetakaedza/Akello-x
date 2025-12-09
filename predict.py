from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PredictRequest(BaseModel):
    student_id: str
    question_id: str
    topic: str
    difficulty: str
    correct: bool
    time_spent_seconds: int

class PredictResponse(BaseModel):
    recommendation: str
    confidence: float
    details: dict

@router.post("/", response_model=PredictResponse)
def predict(req: PredictRequest):
    """
    Simple prototype 'model' (heuristic):
    - if correct and fast => recommend increase_difficulty
    - if wrong and slow  => recommend decrease_difficulty
    - otherwise => same difficulty
    Returns a confidence score between 0.0 and 1.0.
    """
    score = 0.0
    # base from correctness
    if req.correct:
        score += 0.6
    else:
        score += 0.1

    # faster answers increase confidence
    if req.time_spent_seconds <= 20:
        score += 0.25
    elif req.time_spent_seconds <= 45:
        score += 0.1
    elif req.time_spent_seconds >= 90:
        score -= 0.15

    # clamp
    score = max(0.0, min(1.0, score))

    if score >= 0.7:
        recommendation = "increase_difficulty"
    elif score <= 0.25:
        recommendation = "decrease_difficulty"
    else:
        recommendation = "same"

    return PredictResponse(
        recommendation=recommendation,
        confidence=round(score, 2),
        details={"time_spent_seconds": req.time_spent_seconds, "correct": req.correct}
    )
