# Email Sorting OpenEnv 📧

A real-world OpenEnv environment where an AI agent learns to classify
emails as **spam**, **important**, or **promotion**.
Built for the Meta x PyTorch OpenEnv Hackathon.

---

## What This Project Does

In today's world, people receive hundreds of emails daily.
This environment trains an AI agent to automatically sort emails
by reading the subject, body, and sender — just like a smart inbox.

The agent learns:
- Correct classification = **reward**
- Wrong classification = **penalty**
- Harder emails = **higher reward** (to encourage learning)

---

## Environment Details

| Property | Value |
|----------|-------|
| Task Type | Email Classification |
| Action Space | spam / important / promotion |
| Max Steps | 10 per episode |
| Reward Range | -0.5 to +1.0 |
| Difficulty Levels | Easy / Medium / Hard |

---

## Action Space

The agent can take exactly one of these actions per step:

| Action | Meaning |
|--------|---------|
| `spam` | Email is unwanted, scam, or phishing |
| `important` | Email needs attention (work, orders, real alerts) |
| `promotion` | Genuine sale or discount from real shops |

---

## Observation Space

Each step the agent receives:
```json