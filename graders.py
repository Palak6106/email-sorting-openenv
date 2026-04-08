"""
graders.py — Email Sorting OpenEnv
3 grader tasks: easy, medium, hard.
Each grader returns a float score strictly in (0.0, 1.0).
"""


# ============================================
# BASELINE AGENT (default for all graders)
# ============================================

def baseline_agent(email: dict) -> str:
    text = (email.get("subject", "") + " " + email.get("body", "")).lower()
    spam_kw  = ["won", "free", "prize", "claim", "urgent", "congratulations",
                "selected", "suspended", "verify", "overdue", "pre-approved"]
    promo_kw = ["off", "sale", "deal", "discount", "offer", "save",
                "shop", "upgrade", "trial", "rewards", "loyalty"]
    spam_score  = sum(1 for k in spam_kw  if k in text)
    promo_score = sum(1 for k in promo_kw if k in text)
    if spam_score >= 2:   return "spam"
    if promo_score >= 1:  return "promotion"
    return "important"


# ============================================
# TASK 1 — EASY: Obvious spam detection
# ============================================

EASY_EMAILS = [
    {"subject": "You won $1,000,000!", "body": "Click here to claim your prize now.", "label": "spam"},
    {"subject": "FREE iPhone giveaway", "body": "You have been selected. Claim before midnight!", "label": "spam"},
    {"subject": "Congratulations! You're a winner", "body": "Send your details to collect your reward.", "label": "spam"},
    {"subject": "Meeting at 3pm today", "body": "Hi, reminder about our team sync at 3pm.", "label": "important"},
    {"subject": "Your invoice is ready", "body": "Please find your monthly invoice attached.", "label": "important"},
]

def grade_easy_sorting(agent_fn=None) -> float:
    """Returns score strictly in (0.0, 1.0)."""
    if agent_fn is None:
        agent_fn = baseline_agent
    correct = sum(1 for e in EASY_EMAILS if agent_fn(e) == e["label"])
    raw = correct / len(EASY_EMAILS)
    return round(min(0.99, max(0.01, raw)), 2)


# ============================================
# TASK 2 — MEDIUM: Spam + Promotion + Important
# ============================================

MEDIUM_EMAILS = [
    {"subject": "50% off this weekend only!", "body": "Flash sale on all items. Use code SAVE50.", "label": "promotion"},
    {"subject": "New arrivals just for you", "body": "Check out our latest summer collection.", "label": "promotion"},
    {"subject": "Exclusive member offer inside", "body": "As a valued member, enjoy 20% off.", "label": "promotion"},
    {"subject": "Action required: password expiry", "body": "Your password expires in 3 days. Reset it now.", "label": "important"},
    {"subject": "RE: Project update", "body": "Thanks for the update. Let's connect tomorrow.", "label": "important"},
    {"subject": "Urgent: verify your account", "body": "Your account will be suspended. Click to verify.", "label": "spam"},
]

def grade_medium_sorting(agent_fn=None) -> float:
    """Returns score strictly in (0.0, 1.0)."""
    if agent_fn is None:
        agent_fn = baseline_agent
    correct = sum(1 for e in MEDIUM_EMAILS if agent_fn(e) == e["label"])
    raw = correct / len(MEDIUM_EMAILS)
    return round(min(0.99, max(0.01, raw)), 2)


# ============================================
# TASK 3 — HARD: Subtle/tricky emails
# ============================================

HARD_EMAILS = [
    {"subject": "Your account statement", "body": "Your monthly statement from XYZ Bank is ready.", "label": "important"},
    {"subject": "Limited time: upgrade your plan", "body": "Switch to premium and save 30% this month only.", "label": "promotion"},
    {"subject": "Security alert", "body": "A new login was detected from an unknown device.", "label": "important"},
    {"subject": "You have unclaimed rewards", "body": "Collect your loyalty points before they expire.", "label": "promotion"},
    {"subject": "Final notice: payment overdue", "body": "Send $500 to avoid service interruption.", "label": "spam"},
    {"subject": "Team offsite next Friday", "body": "Please confirm your attendance for the offsite.", "label": "important"},
    {"subject": "Claim your free trial", "body": "Start your 30-day free trial — no credit card needed.", "label": "promotion"},
    {"subject": "You've been pre-approved!", "body": "You qualify for a $50,000 loan. Apply now.", "label": "spam"},
]

def grade_hard_sorting(agent_fn=None) -> float:
    """Returns score strictly in (0.0, 1.0)."""
    if agent_fn is None:
        agent_fn = baseline_agent
    correct = sum(1 for e in HARD_EMAILS if agent_fn(e) == e["label"])
    raw = correct / len(HARD_EMAILS)
    return round(min(0.99, max(0.01, raw)), 2)


# ============================================
# RUN ALL GRADERS
# ============================================

def run_all_graders(agent_fn=None):
    if agent_fn is None:
        agent_fn = baseline_agent

    scores = {
        "easy_sorting":   grade_easy_sorting(agent_fn),
        "medium_sorting": grade_medium_sorting(agent_fn),
        "hard_sorting":   grade_hard_sorting(agent_fn),
    }
    avg = round(sum(scores.values()) / len(scores), 4)
    print(f"[GRADER] easy={scores['easy_sorting']} medium={scores['medium_sorting']} hard={scores['hard_sorting']} avg={avg}", flush=True)
    return {"scores": scores, "average_score": avg}


if __name__ == "__main__":
    print("Running all graders with baseline agent...\n")
    results = run_all_graders()
    for task_id, score in results["scores"].items():
        print(f"Task: {task_id:20s} | Score: {score}")
    print(f"\nAverage Score: {results['average_score']}")
