# 🤖 Multi-Agent Orchestration Platform

> Supervisory multi-agent system routing across 7 specialized agents using AWS Bedrock + LangChain

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=flat&logo=chainlink&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=flat&logo=aws-lambda&logoColor=white)

---

## 📋 Overview

A production-grade multi-agent orchestration platform built on AWS Bedrock and LangChain. A supervisor agent dynamically routes tasks to 7 specialized sub-agents based on task classification, enabling modular and extensible AI workflows.

---

## ✨ Features

- **Supervisor Routing** — Intelligent task classification and routing across 7 specialized agents
- **6 Extensible Python Tools** — Modular tool APIs (web search, data retrieval, summarization, code execution, etc.)
- **Persona-Based Prompting** — Modular system-prompt templates per agent persona for consistent behavior
- **Serverless Scoring API** — Candidate-scoring REST API deployed on AWS Lambda
- **Scalable Architecture** — Stateless, event-driven design ready for production scaling

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌──────────────────┐
│  Supervisor Agent │  ← Task Classification & Routing
└──────────────────┘
    │         │         │
    ▼         ▼         ▼
Agent_1   Agent_2   Agent_3  ...  Agent_7
(Role A)  (Role B)  (Role C)      (Role G)
    │
    ▼
Python Tool APIs (x6)
    │
    ▼
AWS Lambda (Scoring API)
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangChain Agents |
| LLM Provider | AWS Bedrock (Claude / Titan) |
| Tool APIs | Python (FastAPI) |
| Serverless API | AWS Lambda |
| Orchestration | LangGraph / LangChain |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/Dhanunjaychowdary/multi-agent-orchestration-platform.git
cd multi-agent-orchestration-platform

# Install dependencies
pip install -r requirements.txt

# Set up AWS credentials
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Run the orchestration platform
python main.py
```

---

## 📁 Project Structure

```
multi-agent-orchestration-platform/
├── agents/
│   ├── supervisor.py        # Supervisor routing logic
│   ├── agent_registry.py    # Agent definitions & personas
│   └── specialized/         # 7 specialized agent modules
├── tools/
│   ├── tool_registry.py     # 6 extensible Python tools
│   └── ...
├── api/
│   └── lambda_handler.py    # AWS Lambda scoring API
├── prompts/
│   └── system_prompts/      # Per-persona prompt templates
├── requirements.txt
└── main.py
```

---

## 📊 Results

- Supervisory routing across **7 specialized agents**
- **6 extensible Python tools** exposed via APIs
- Serverless candidate-scoring API on **AWS Lambda**
- Modular system-prompt templates per agent persona

---

*Built by [Dhanunjaya Nimmagadda](https://github.com/Dhanunjaychowdary) — AI Research Engineer*
