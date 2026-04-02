from env import EmailSortingEnv, EMAILS
from typing import Dict

# ============================================
# GRADER 1 — EASY TASK
# ============================================

def grade_easy_task() -> Dict:
    """
    Easy Task: Sort obviously spam emails correctly.
    Tests if the agent can catch simple scam/prize emails.
    Score: 0.0 to 1.0
    """
    env = EmailSortingEnv()
    easy_emails = [e for e in EMAILS if e["difficulty"] == "easy"]

    correct = 0
    total = len(easy_emails)

    for email in easy_emails:
        # Simulate agent decision using simple keyword rules
        subject = email["subject"].lower()
        body = email["body"].lower()
        sender = email["sender"].lower()

        # Simple rule-based agent for testing
        spam_keywords = ["won", "free", "prize", "urgent", "money", "congratulations",
                        "click here", "earn", "selected", "claim"]

        score_spam = sum(1 for kw in spam_keywords if kw in subject or kw in body)

        if score_spam >= 2:
            action = "spam"
        else:
            action = "important"

        if action == email["label"]:
            correct += 1

    final_score = round(correct / total, 2) if total > 0 else 0.0

    return {
        "task": "easy_sorting",
        "difficulty": "easy",
        "description": "Sort obvious spam emails",
        "correct": correct,
        "total": total,
        "score": final_score,
        "passed": final_score >= 0.5
    }


# ============================================
# GRADER 2 — MEDIUM TASK
# ============================================

def grade_medium_task() -> Dict:
    """
    Medium Task: Distinguish newsletters, promotions, important emails.
    Tests if the agent understands context beyond just spam detection.
    Score: 0.0 to 1.0
    """
    env = EmailSortingEnv()
    medium_emails = [e for e in EMAILS if e["difficulty"] == "medium"]

    correct = 0
    total = len(medium_emails)

    for email in medium_emails:
        subject = email["subject"].lower()
        body = email["body"].lower()
        sender = email["sender"].lower()

        # Medium level agent logic
        promotion_keywords = ["off", "sale", "deal", "discount", "shop", "offer", "save"]
        important_keywords = ["order", "shipped", "newsletter", "weekly", "stories",
                             "dispatched", "track", "account"]

        promo_score = sum(1 for kw in promotion_keywords if kw in subject or kw in body)
        imp_score = sum(1 for kw in important_keywords if kw in subject or kw in body)

        if promo_score > imp_score:
            action = "promotion"
        elif imp_score > 0:
            action = "important"
        else:
            action = "spam"

        if action == email["label"]:
            correct += 1

    final_score = round(correct / total, 2) if total > 0 else 0.0

    return {
        "task": "medium_sorting",
        "difficulty": "medium",
        "description": "Distinguish newsletters vs promotions vs important",
        "correct": correct,
        "total": total,
        "score": final_score,
        "passed": final_score >= 0.5
    }


# ============================================
# GRADER 3 — HARD TASK
# ============================================

def grade_hard_task() -> Dict:
    """
    Hard Task: Detect phishing emails disguised as banks/trusted services.
    Tests if the agent can catch sophisticated scams.
    Score: 0.0 to 1.0
    """
    env = EmailSortingEnv()
    hard_emails = [e for e in EMAILS if e["difficulty"] == "hard"]

    correct = 0
    total = len(hard_emails)

    for email in hard_emails:
        subject = email["subject"].lower()
        body = email["body"].lower()
        sender = email["sender"].lower()

        # Hard level — check suspicious domains
        suspicious_domains = [".xyz", ".tk", ".net", ".org", "-secure", "-alert",
                              "login", "verify", "suspended", "action required"]
        trusted_domains = ["@company.com", "@gmail.com", "@yahoo.com"]

        phishing_score = sum(1 for kw in suspicious_domains if kw in sender or kw in body)
        trusted_score = sum(1 for d in trusted_domains if d in sender)

        urgency_words = ["suspended", "verify", "action required", "immediately",
                        "stop", "urgent"]
        urgency_score = sum(1 for w in urgency_words if w in subject or w in body)

        if phishing_score >= 2 or (urgency_score >= 1 and trusted_score == 0):
            action = "spam"
        elif trusted_score > 0:
            action = "important"
        else:
            action = "promotion"

        if action == email["label"]:
            correct += 1

    final_score = round(correct / total, 2) if total > 0 else 0.0

    return {
        "task": "hard_sorting",
        "difficulty": "hard",
        "description": "Detect phishing and sophisticated scam emails",
        "correct": correct,
        "total": total,
        "score": final_score,
        "passed": final_score >= 0.5
    }


# ============================================
# RUN ALL GRADERS
# ============================================

def run_all_graders() -> Dict:
    """Run all 3 graders and return combined results."""
    print("Running all graders...\n")

    easy_result = grade_easy_