---
title: Email Sorting Openenv
emoji: 📧
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
tags:
  - openenv
---

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
{
  "email": {
    "subject": "You won $1,000,000!",
    "body": "Click here to claim your prize.",
    "sender": "prize@randomsite.xyz"
  },
  "step": 1,
  "max_steps": 10,
  "total_reward": 0.0,
  "done": false,
  "valid_actions": ["spam", "important", "promotion"]
}
```

---

## Tasks

| Task | Difficulty | Description | Expected Score |
|------|------------|-------------|----------------|
| `easy_sorting` | Easy | Classify obvious spam vs important emails | 0.6 – 0.8 |
| `medium_sorting` | Medium | Distinguish spam, promotion, and important | 0.5 – 0.7 |
| `hard_sorting` | Hard | Detect subtle phishing and tricky promotions | 0.4 – 0.6 |

---

## Reward Function

| Event | Reward |
|-------|--------|
| Easy correct | +0.5 |
| Medium correct | +0.75 |
| Hard correct | +1.0 |
| Easy wrong | -0.5 |
| Medium wrong | -0.3 |
| Hard wrong | -0.1 |
| Invalid action | -0.2 |

---

## Baseline Scores

Scores achieved by the rule-based baseline agent (`baseline_agent` in `graders.py`):

| Task | Score |
|------|-------|
| easy_sorting | 0.8 |
| medium_sorting | 0.67 |
| hard_sorting | 0.5 |
| **Average** | **0.657** |

---

## Setup & Usage

### Local

```bash
pip install -r requirements.txt
python server.py           # starts server at http://localhost:7860
python graders.py          # run graders with baseline agent
python inference.py        # run inference loop
```

### Docker

```bash
docker build -t email-sorting-openenv .
docker run -p 7860:7860 email-sorting-openenv
```

### API

```bash
curl -X POST http://localhost:7860/reset
curl -X POST http://localhost:7860/step -H "Content-Type: application/json" -d '{"action":"spam"}'
curl http://localhost:7860/state
curl http://localhost:7860/graders
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | LLM API base URL | `https://api.openai.com/v1` |
| `MODEL_NAME` | Model to use | `gpt-4o-mini` |
| `HF_TOKEN` | HuggingFace / API token | — |