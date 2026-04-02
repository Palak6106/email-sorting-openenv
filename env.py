import random
from typing import Dict, Any, Tuple

# Sample emails dataset
EMAILS = [
    # Easy - Obvious spam
    {"subject": "YOU WON $1,000,000!!!", "body": "Click here to claim your prize money now!", "sender": "prize@randomsite.xyz", "label": "spam", "difficulty": "easy"},
    {"subject": "FREE iPhone 15 for you!", "body": "Congratulations! You have been selected. Send your details.", "sender": "free@giveaway123.com", "label": "spam", "difficulty": "easy"},
    {"subject": "URGENT: Make money fast", "body": "Work from home earn 50000 per day no experience needed.", "sender": "jobs@quickmoney.tk", "label": "spam", "difficulty": "easy"},

    # Medium - Newsletter vs Promotion
    {"subject": "Your weekly newsletter", "body": "Here are this week's top stories in technology and science.", "sender": "newsletter@techdigest.com", "label": "important", "difficulty": "medium"},
    {"subject": "50% OFF this weekend only!", "body": "Shop now and save big on electronics. Limited time offer.", "sender": "deals@amazon.com", "label": "promotion", "difficulty": "medium"},
    {"subject": "Your order has been shipped", "body": "Your recent order #12345 has been dispatched. Track here.", "sender": "orders@flipkart.com", "label": "important", "difficulty": "medium"},

    # Hard - Phishing disguised as bank
    {"subject": "Your SBI account is suspended", "body": "Dear customer, your account is suspended. Login immediately at sbi-secure-login.xyz", "sender": "support@sbi-alerts.net", "label": "spam", "difficulty": "hard"},
    {"subject": "Action required: Verify your UPI", "body": "Your UPI ID needs verification. Click here to verify now or service will stop.", "sender": "noreply@paytm-secure.org", "label": "spam", "difficulty": "hard"},
    {"subject": "Meeting rescheduled to 3pm", "body": "Hi, just wanted to let you know the team meeting is moved to 3pm today.", "sender": "manager@company.com", "label": "important", "difficulty": "hard"},
]

CATEGORIES = ["spam", "important", "promotion"]

class EmailSortingEnv:
    def __init__(self):
        self.current_email = None
        self.current_step = 0
        self.max_steps = 10
        self.total_reward = 0.0
        self.done = False
        self.history = []

    def reset(self) -> Dict[str, Any]:
        """Reset environment to start a new episode."""
        self.current_step = 0
        self.total_reward = 0.0
        self.done = False
        self.history = []
        self.current_email = random.choice(EMAILS)
        return self.state()

    def state(self) -> Dict[str, Any]:
        """Return current state of the environment."""
        if self.current_email is None:
            self.reset()
        return {
            "email": {
                "subject": self.current_email["subject"],
                "body": self.current_email["body"],
                "sender": self.current_email["sender"]
            },
            "step": self.current_step,
            "max_steps": self.max_steps,
            "total_reward": round(self.total_reward, 2),
            "done": self.done,
            "valid_actions": CATEGORIES
        }

    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, Dict]:
        """
        Take a step: classify the email.
        action: one of 'spam', 'important', 'promotion'
        Returns: (next_state, reward, done, info)
        """
        if self.done:
            return self.state(), 0.0, True, {"error": "Episode already done. Call reset()."}

        if action not in CATEGORIES:
            reward = -0.2
            info = {"error": f"Invalid action. Choose from {CATEGORIES}"}
        else:
            correct_label = self.current_email["label"]
            difficulty = self.current_email["difficulty"]

            if action == correct_label:
                # Reward based on difficulty
                if difficulty == "easy":
                    reward = 0.5
                elif difficulty == "medium":
                    reward = 0.75
                else:  # hard
                    reward = 1.0
                info = {"result": "correct", "difficulty": difficulty}
            else:
                # Penalty
                if difficulty == "easy":
                    reward = -0.5
                elif difficulty == "medium":
                    reward = -0.3
                else:
                    reward = -0.1
                info = {"result": "wrong", "correct_label": correct_label, "difficulty": difficulty}

        self.total_reward += reward
        self.current_step += 1
        self.history.append({
            "step": self.current_step,
            "email_subject": self.current_email["subject"],
            "action": action,
            "reward": reward
        })

        # Move to next email
        if self.current_step >= self.max_steps:
            self.done = True
        else:
            self.current_email = random.choice(EMAILS)

        return self.state(), round(reward, 2), self.done, info


# For testing - run this file directly
if __name__ == "__main__":
    env = EmailSortingEnv()
    state = env.reset()
    print("=== Email Sorting Environment Test ===")
    print(f"Email: {state['email']['subject']}")
    print(f"From: {state['email']['sender']}")

    next_state, reward, done, info = env.step("spam")
    print(f"\nAction: spam")
    print(f"Reward: {reward}")
    print(f"Result: {info}")
    print("\nenv.py is working correctly!")