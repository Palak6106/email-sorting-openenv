import os
import json
from openai import OpenAI
from env import EmailSortingEnv

# ============================================
# SETUP — Read environment variables
# ============================================

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN if HF_TOKEN else "dummy-key"
)

# ============================================
# AI AGENT — Asks LLM to classify email
# ============================================

def ask_llm_to_classify(email: dict) -> str:
    """
    Send email to LLM and get classification.
    Returns: 'spam', 'important', or 'promotion'
    """

    prompt = f"""You are an email classification assistant.

Classify the following email into exactly ONE of these categories:
- spam: unwanted, scam, phishing, prize winning, fake offers
- important: work emails, order updates, bank alerts from real banks, newsletters
- promotion: genuine sale offers, discount emails from real shops

Email Details:
Subject: {email['subject']}
From: {email['sender']}
Body: {email['body']}

Reply with ONLY one word — either: spam, important, or promotion
Do not explain. Just one word."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an email classifier. Reply with only one word: spam, important, or promotion."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=10,
            temperature=0.0
        )

        # Extract the answer
        answer = response.choices[0].message.content.strip().lower()

        # Clean up answer — only keep valid categories
        if "spam" in answer:
            return "spam"
        elif "promotion" in answer:
            return "promotion"
        elif "important" in answer:
            return "important"
        else:
            return "spam"  # Default fallback

    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback to simple rule-based classification
        return fallback_classify(email)


def fallback_classify(email: dict) -> str:
    """
    Simple rule-based fallback if LLM fails.
    """
    subject = email["subject"].lower()
    body = email["body"].lower()
    sender = email["sender"].lower()

    spam_keywords = ["won", "free", "prize", "urgent", "money",
                    "congratulations", "claim", "earn", "selected",
                    "suspended", "verify", "action required"]

    promo_keywords = ["off", "sale", "deal", "discount", "shop",
                     "offer", "save", "limited time"]

    spam_score = sum(1 for kw in spam_keywords if kw in subject or kw in body)
    promo_score = sum(1 for kw in promo_keywords if kw in subject or kw in body)

    suspicious_domain = any(d in sender for d in [".xyz", ".tk", "-secure", "-alert"])

    if spam_score >= 2 or suspicious_domain:
        return "spam"
    elif promo_score >= 2:
        return "promotion"
    else:
        return "important"


# ============================================
# MAIN INFERENCE LOOP
# ============================================

def run_inference():
    """
    Main function — runs the AI agent for one full episode.
    """
    print("=" * 50)
    print("Email Sorting Environment — Inference Script")
    print("=" * 50)
    print(f"Model: {MODEL_NAME}")
    print(f"API Base: {API_BASE_URL}")
    print("=" * 50)

    # Initialize environment
    env = EmailSortingEnv()
    state = env.reset()

    print(f"\nStarting episode — max {state['max_steps']} steps\n")

    step_results = []

    # Run until episode is done
    while not state["done"]:
        current_step = state["step"] + 1
        email = state["email"]

        print(f"Step {current_step}/{state['max_steps']}")
        print(f"Subject: {email['subject']}")
        print(f"From:    {email['sender']}")

        # Ask AI to classify
        action = ask_llm_to_classify(email)
        print(f"AI Decision: {action}")

        # Take step in environment
        next_state, reward, done, info = env.step(action)

        print(f"Reward: {reward} | Result: {info.get('result', 'N/A')}")
        print("-" * 40)

        step_results.append({
            "step": current_step,
            "subject": email["subject"],
            "action": action,
            "reward": reward,
            "result": info.get("result", "N/A")
        })

        state = next_state

    # ============================================
    # FINAL RESULTS
    # ============================================

    total_reward = state["total_reward"]
    total_steps = state["step"]
    correct_count = sum(1 for r in step_results if r["result"] == "correct")

    print("\n" + "=" * 50)
    print("EPISODE COMPLETE")
    print("=" * 50)
    print(f"Total Steps:    {total_steps}")
    print(f"Correct:        {correct_count}/{total_steps}")
    print(f"Accuracy:       {round(correct_count/total_steps*100, 1)}%")
    print(f"Total Reward:   {total_reward}")
    print("=" * 50)

    # Save results to file
    results = {
        "model": MODEL_NAME,
        "total_steps": total_steps,
        "correct": correct_count,
        "accuracy": round(correct_count / total_steps * 100, 1),
        "total_reward": total_reward,
        "step_details": step_results
    }

    with open("inference_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to inference_results.json")
    return results


# ============================================
# RUN GRADERS ALSO
# ============================================

def run_with_graders():
    """Run inference + all graders and show combined score."""
    from graders import run_all_graders

    print("\n--- Running Inference ---\n")
    inference_results = run_inference()

    print("\n--- Running Graders ---\n")
    grader_results = run_all_graders()

    print("\n" + "=" * 50)
    print("FINAL COMBINED RESULTS")
    print("=" * 50)
    print(f"Inference Accuracy: {inference_results['accuracy']}%")
    print(f"Grader Average Score: {grader_results['average_score']}")
    print(f"All Graders Passed: {grader_results['all_passed']}")
    print("=" * 50)


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    run_with_graders()
