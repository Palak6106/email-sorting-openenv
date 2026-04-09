import os
from openai import OpenAI
from env import EmailSortingEnv

# ============================================
# SETUP — Read environment variables
# ============================================

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN     = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# ============================================
# AI AGENT — Asks LLM to classify email
# ============================================

def ask_llm_to_classify(email: dict) -> str:
    prompt = f"""You are an email classification assistant.
Classify the following email into exactly ONE of these categories:
- spam: unwanted, scam, phishing, prize winning, fake offers
- important: work emails, order updates, bank alerts, urgent notices
- promotion: genuine sale offers, discount emails from real shops

Subject: {email['subject']}
From: {email['sender']}
Body: {email['body']}

Reply with ONLY one word: spam, important, or promotion"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an email classifier. Reply with only one word: spam, important, or promotion."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.0
        )
        answer = response.choices[0].message.content.strip().lower()
        if "spam" in answer:        return "spam"
        elif "promotion" in answer: return "promotion"
        elif "important" in answer: return "important"
        else:                       return "spam"
    except Exception as e:
        return fallback_classify(email)


def fallback_classify(email: dict) -> str:
    subject = email["subject"].lower()
    body    = email["body"].lower()
    sender  = email["sender"].lower()

    spam_kw  = ["won", "free", "prize", "urgent", "money", "congratulations",
                "claim", "earn", "selected", "suspended", "verify"]
    promo_kw = ["off", "sale", "deal", "discount", "shop", "offer", "save", "limited time"]

    spam_score  = sum(1 for kw in spam_kw  if kw in subject or kw in body)
    promo_score = sum(1 for kw in promo_kw if kw in subject or kw in body)
    suspicious  = any(d in sender for d in [".xyz", ".tk", "-secure", "-alert"])

    if spam_score >= 2 or suspicious: return "spam"
    elif promo_score >= 2:             return "promotion"
    else:                              return "important"


# ============================================
# MAIN INFERENCE LOOP
# ============================================

def run_inference():
    env   = EmailSortingEnv()
    state = env.reset()

    rewards      = []
    step_results = []
    error        = None

    # [START] — required format
    print(f"[START] task=email_sorting env=email-sorting-openenv model={MODEL_NAME}", flush=True)

    try:
        while not state["done"]:
            current_step = state["step"] + 1
            email        = state["email"]

            action = ask_llm_to_classify(email)

            next_state, reward, done, info = env.step(action)

            error_msg = info.get("error", "null") or "null"
            done_str  = "true" if done else "false"

            # [STEP] — exact required format
            print(f"[STEP] step={current_step} action={action} reward={reward:.2f} done={done_str} error={error_msg}", flush=True)

            rewards.append(reward)
            step_results.append({"step": current_step, "action": action, "reward": reward, "result": info.get("result", "N/A")})

            state = next_state

        success = True

    except Exception as e:
        error   = str(e)
        success = False

    # [END] — exact required format
    total_steps   = len(rewards)
    rewards_str   = ",".join(f"{r:.2f}" for r in rewards)
    success_str   = "true" if success else "false"
    print(f"[END] success={success_str} steps={total_steps} rewards={rewards_str}", flush=True)

    return {
        "model":        MODEL_NAME,
        "total_steps":  total_steps,
        "total_reward": round(sum(rewards), 2),
        "success":      success,
        "step_details": step_results
    }


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    run_inference()
