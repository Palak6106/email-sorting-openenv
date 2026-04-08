import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from env import EmailSortingEnv

app = FastAPI(
    title="Email Sorting OpenEnv",
    description="Real-world email sorting environment for RL agents",
    version="1.0.0"
)

env = EmailSortingEnv()

# ============================================
# PYDANTIC MODELS — typed Observation, Action, Reward
# ============================================

class EmailModel(BaseModel):
    subject: str
    body: str
    sender: str

class Observation(BaseModel):
    email: EmailModel
    step: int
    max_steps: int
    total_reward: float
    done: bool
    valid_actions: List[str]

class StepRequest(BaseModel):
    action: str

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]

class ResetResponse(BaseModel):
    observation: Observation

class GraderTask(BaseModel):
    task_id: str
    score: float

class GradersResponse(BaseModel):
    tasks: List[GraderTask]
    average_score: float

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Email Sorting Environment is running"}

@app.get("/")
def root():
    return {
        "name": "Email Sorting OpenEnv",
        "version": "1.0.0",
        "description": "Sort emails as spam, important, or promotion",
        "endpoints": ["/reset", "/step", "/state", "/graders", "/health"]
    }

@app.post("/reset", response_model=ResetResponse)
def reset():
    """Reset environment and return initial observation."""
    state = env.reset()
    return ResetResponse(observation=Observation(**state))

@app.post("/step", response_model=StepResponse)
def step(request: StepRequest):
    """Take action and return next observation, reward, done, info."""
    next_state, reward, done, info = env.step(request.action)
    return StepResponse(
        observation=Observation(**next_state),
        reward=reward,
        done=done,
        info=info
    )

@app.get("/state", response_model=ResetResponse)
def get_state():
    """Return current observation without taking action."""
    return ResetResponse(observation=Observation(**env.state()))

@app.get("/graders", response_model=GradersResponse)
def run_graders():
    """Run all graders and return scores."""
    from graders import grade_easy_sorting, grade_medium_sorting, grade_hard_sorting
    tasks = [
        GraderTask(task_id="easy_sorting",   score=grade_easy_sorting()),
        GraderTask(task_id="medium_sorting",  score=grade_medium_sorting()),
        GraderTask(task_id="hard_sorting",    score=grade_hard_sorting()),
    ]
    avg = round(sum(t.score for t in tasks) / len(tasks), 4)
    return GradersResponse(tasks=tasks, average_score=avg)

@app.get("/graders/easy_sorting")
def grade_easy():
    from graders import grade_easy_sorting
    return {"task_id": "easy_sorting", "score": grade_easy_sorting()}

@app.get("/graders/medium_sorting")
def grade_medium():
    from graders import grade_medium_sorting
    return {"task_id": "medium_sorting", "score": grade_medium_sorting()}

@app.get("/graders/hard_sorting")
def grade_hard():
    from graders import grade_hard_sorting
    return {"task_id": "hard_sorting", "score": grade_hard_sorting()}

# ============================================
# START SERVER
# ============================================

if __name__ == "__main__":
    print("Starting Email Sorting Environment Server...")
    print("Server running at http://localhost:7860")
    uvicorn.run(app, host="0.0.0.0", port=7860)
