# HomeChef – AI-Powered Desktop Recipe Assistant (Starter)

This is a **starter project** scaffold for the HomeChef desktop app built with **Python**, **PySide6 (Qt)**, **SQLite**, and the **OpenAI API**.

## Quick Start (Windows / macOS / Linux)
1) Install Python 3.10+ and VS Code.
2) In VS Code Terminal:
   ```bash
   cd HomeChef
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3) Create `.env` from `.env.example` and set `OPENAI_API_KEY`.
4) Seed the database:
   ```bash
   python -m src.homechef.seed_db
   ```
5) Run the app:
   ```bash
   python -m src.homechef.app
   ```

## Packaging (optional)
You can bundle an executable later with PyInstaller:
```bash
pip install pyinstaller
pyinstaller -F -w -n HomeChef src/homechef/app.py
```

---
**Note:** The OpenAI tab requires a valid API key and internet connection.
