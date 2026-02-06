# CARA-Bot ⚖️

**Contract Analysis & Risk Assessment Bot**

CARA-Bot is an AI-powered, local-first legal assistant designed to help Small and Medium Enterprises (SMEs) and individuals analyze contracts, detect risks, and understand complex legal language.

It combines **rule-based logic** for deterministic risk detection with **LLM capabilities (Groq)** for plain-language explanations, ensuring both accuracy and accessibility.

---

## 🚀 Key Features

*   **📄 Universal Support**: Upload PDF, DOCX, or TXT files.
*   **🔍 Automatic Analysis**:
    *   **Classifies** contract types (Employment, NDA, Service Agreement, etc.).
    *   **Extracts** key clauses.
    *   **Detects** high-risk terms using a robust rule engine.
*   **⚠️ Risk Assessment**:
    *   Flags critical and high-severity risks.
    *   Highlights specific problematic clauses.
*   **🤖 AI Explanations**:
    *   Integration with **Groq** (using `openai/gpt-oss-120b` or similar models) to explain risks in simple English.
    *   Provides business impact analysis and alternative wording.
*   **📥 PDF Reporting**: Export a professional risk assessment report with a single click.
*   **🔒 Privacy Focused**: All core analysis happens locally. LLM calls are optional and only sent for specific "Explain" requests.

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **Backend**: Python
*   **Package Management**: `uv` (modern Python package manager)
*   **AI/LLM**: Groq API
*   **PDF Generation**: ReportLab
*   **NLP/Parsing**: `pdfplumber`, `python-docx`

---

## ⚙️ Installation & Setup

### Prerequisites
*   Python 3.10 or higher
*   [uv](https://github.com/astral-sh/uv) (Recommended) or `pip`

### 1. Clone the Repository
```bash
git clone https://github.com/santhoshkumar0810/CARA-Bot.git
cd CARA-Bot
```

### 2. Install Dependencies
Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -e .
```

### 3. Configure Environment
Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API=your_groq_api_key_here
```

> **Note**: You can get a free API key from [Groq Console](https://console.groq.com/).

---

## ▶️ Usage

Run the application using the main entry script:

```bash
uv run main.py
```
*(Or `python main.py` if using standard pip)*

1.  Open the local URL provided (usually `http://localhost:8501`).
2.  **Upload** a contract file (PDF/DOCX).
3.  Click **"🚀 Analyze Contract"**.
4.  View risks, explore clauses, and request AI explanations for specific warnings.
5.  Click **"📥 Download Risk Report"** to save the findings.

---

## 📂 Project Structure

```
CARA-Bot/
├── clause_classifier/    # Logic to classify clause types
├── clause_extraction/    # RegEx patterns to split text into clauses
├── contract_classifier/  # Logic to determine contract type
├── export/               # PDF report generation logic
├── ingestion/            # Readers for PDF and DOCX
├── intent_detection/     # Identifies the intent of clauses
├── language/             # Language detection
├── llm_explainer/        # Groq integration for explanations
├── preprocessing/        # Text cleaning and normalization
├── risk_engine/          # Rule-based risk evaluation
├── ui/                   # Streamlit application interface
├── main.py               # Application entry point
├── pyproject.toml        # Dependencies and configuration
└── README.md             # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source.
