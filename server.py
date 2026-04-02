import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env import EmailSortingEnv

# Create FastAPI app
app = FastAPI(
    title="Email Sorting OpenEnv",
    description="Real-world email sorting environment for RL agents",
    version="1.0.0"
)

# One global environment instance
env = EmailSortingEnv()

# ============================================
# REQUEST MODELS
# ============================================

class StepRequest(BaseModel):
    action: str

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/health")
def health_check():
    """Health check — must return 200."""
    return {"status": "ok", "message": "Email Sorting Environment is running"}

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Email Sorting OpenEnv",
        "version": "1.0.0",
        "description": "Sort emails as spam, important, or promotion",
        "endpoints": ["/reset", "/step", "/state", "/health"]
    }

@app.post("/reset")
def reset():
    """Reset environment and return initial state."""
    state = env.reset()
    return {
        "status": "success",
        "state": state
    }

@app.post("/step")
def step(request: StepRequest):
    """
    Take action in environment.
    Body: {"action": "spam"} or {"action": "important"} or {"action": "promotion"}
    """
    next_state, reward, done, info = env.step(request.action)
    return {
        "status": "success",
        "state": next_state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def get_state():
    """Return current state without taking action."""
    return {
        "status": "success",
        "state": env.state()
    }

@app.get("/graders")
def run_graders():
    """Run all graders and return scores."""
    from graders import run_all_graders
    results = run_all_graders()
    return {
        "status": "success",
        "results": results
    }

# ============================================
# START SERVER
# ============================================

if __name__ == "__main__":
    print("Starting Email Sorting Environment Server...")
    print("Server running at http://localhost:7860")
    uvicorn.run(app, host="0.0.0.0", port=7860)