# 🧑‍🍳 HomeChef – AI-Powered Desktop Recipe Assistant

**HomeChef** is an intelligent desktop application designed to revolutionize the home cooking experience. By leveraging the **ultra-fast Groq API**, this assistant helps users discover meals based on ingredients they already have, provides real-time contextual cooking guidance, and manages dynamic grocery lists.

---

## 🚀 Features & Core Modules

This application transforms meal planning and cooking through five core modules:

| Module | Description | Key Functionality |
| :--- | :--- | :--- |
| **Recipe Management** | A browsable and searchable library containing detailed recipes, instructions, and cooking metrics. | Allows users to save favorites and access clear, step-by-step guides. |
| **Smart Recipe Suggestions** | Uses AI to generate meal ideas based on the ingredients the user has on hand. | Suggests matching database recipes or generates creative ideas if no direct match is found. |
| **AI Cooking Assistant** | An interactive chatbot powered by the **Groq API** for context-aware help. | Provides real-time guidance, ingredient substitution advice, and general cooking tips. |
| **Grocery List Management** | Automatically manages shopping lists based on selected recipes and pantry contents. | Auto-identifies missing ingredients and allows manual addition/removal. |
| **Real-time Guide** | Presents recipe instructions clearly while cooking, with the option to ask the AI for contextual tips. | Simplifies the cooking process and reduces mistakes in the kitchen. |

---

## ⚙️ Suggested Tools & Technologies

* **Programming Language:** Python (for backend logic and GUI control)
* **Desktop GUI:** PyQt / PySide6 (Recommended)
* **Database:** SQLite (Serverless, file-based storage for recipes)
* **Core AI API:** **Groq API** (For intelligent recipe generation and chatbot responses)

---

## ⚡ Quick Start (Setup & Run)

This guide helps you set up the **HomeChef** starter project locally.

1.  **Install Python 3.10+** and Git.
2.  Navigate to the project root directory in your terminal.
3.  **Create and Activate a virtual environment:**
    ```bash
    python -m venv .venv

    # Windows PowerShell:
    .venv\Scripts\Activate
    # macOS/Linux/Git Bash:
    source .venv/bin/activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure API Key:**
    * Create a copy of `.env.example` and name it **`.env`**.
    * Edit the `.env` file and set your **GROQ\_API\_KEY**. (The value should be empty in your GitHub file!)

6.  **Seed the database** with initial recipes:
    ```bash
    python -m src.homechef.seed_db
    ```
7.  **Run the application:**
    ```bash
    python -m src.homechef.app
    ```

---

## 📦 Packaging (Optional)

You can bundle the application into a standalone executable file using PyInstaller:

```bash
pip install pyinstaller
pyinstaller -F -w -n HomeChef src/homechef/app.py
