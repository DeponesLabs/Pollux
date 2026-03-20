# Pollux
![Status: Under Development](https://img.shields.io/badge/Status-Under%20Development-orange?style=for-the-badge)

**Pollux** is a minimalist, modular, and high-performance terminal client built for **Google's Gemini AI models**. 

Named after one of the twin stars in the **Gemini constellation**, Pollux serves as the "brighter twin"—a core engine designed to provide a clean, developer-centric interface for interacting with Large Language Models (LLMs) directly from the terminal.

---

## Key Features

* **Modular Architecture:** Built with strict Object-Oriented Programming (OOP) principles, allowing easy integration and extension.
* **Type-Safe Model Management:** Leverages Python Enums and Dataclasses for robust handling of Gemini model versions (Pro, Flash, Thinking).
* **Granular Safety Control:** Direct access to Google’s safety settings, allowing developers to toggle filtering thresholds (e.g., `BLOCK_NONE`).
* **Automated Cataloging:** Automatically fetches and exports available model metadata to a structured JSON database for offline reference.
* **Developer-First Design:** Optimized for low latency and high readability, making it an ideal "Proof of Work" for AI integration.

---

## Tech Stack

* **Language:** Python 3.10+
* **AI Engine:** [Google GenAI SDK](https://github.com/google-gemini/generative-ai-python)
* **Environment:** Terminal / CLI
* **Data Handling:** JSON, Dataclasses (with `slots=True` for memory efficiency)

---

## Project Structure

Pollux follows a **Core & Extension** architecture. This repository contains the **Core** version.

```text
Pollux/
├── src/
│   └── pollux/
│       ├── client.py     # Main API logic and session management
│       ├── models.py     # Dataclass representations of AI models
│       └── enums.py      # Type-safe model and safety definitions
├── gemini_models_catalog.json # Auto-generated model database
├── .env                  # API Key configuration (ignored by git)
└── main.py               # Minimalist entry point
```

---

## Getting Started

### 1. Prerequisites
Get your API Key from [Google AI Studio](https://aistudio.google.com/).

### 2. Installation
```bash
git clone https://github.com/DeponesLabs/Pollux.git
cd Pollux
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_api_key_here
```

### 4. Run Pollux
```bash
python main.py
```

---

## Safety Configuration

Pollux allows you to override default safety filters for research and specialized development purposes:

```python
# Example: Setting safety threshold to allow all content
client.set_safety_config(
    dangerous_content=types.HarmBlockThreshold.BLOCK_NONE
)
```

---

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it in both open-source and commercial projects.
