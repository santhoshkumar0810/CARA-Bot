import streamlit as st
import os
import sys

# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.pdf_reader import read_pdf
from ingestion.docx_reader import read_docx
from preprocessing.text_cleaner import clean_text
from language.detect_language import detect_language_code
from clause_extraction.extract_clauses import extract_clauses_from_text
from contract_classifier.classify_contract_type import classify_contract_type
from clause_classifier.rule_based import classify_clause_rule_based
from intent_detection.intent_rules import detect_clause_intent
from risk_engine.risk_evaluator import load_risk_rules, evaluate_risk
from llm_explainer.explain_clause import generate_clause_explanation
from export.pdf_report import generate_pdf_report


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="CARA-Bot | Contract Risk Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------------------------
# GLOBAL STYLES (DARK/LIGHT SAFE)
# ---------------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f6f8fb !important;
    padding: 25px 40px;
}
h1 {
    font-size: 42px;
    font-weight: 700;
    /* Color removed for dark mode compatibility */
}
.subtitle {
    font-size: 18px;
    opacity: 0.8;
    margin-bottom: 25px;
}
.card {
     /* background-color: #ffffff !important; */
     /* color: #111827 !important; */
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    border: 1px solid rgba(255,255,255,0.1);
}
.metric h3 {
    font-size: 14px;
    opacity: 0.7;
}
.metric p {
    font-size: 26px;
    font-weight: 700;
}
.risk-card {
    /* background-color: #ffffff !important; */
    /* color: #111827 !important; */
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}
.high { border-left: 6px solid #dc2626; }
.medium { border-left: 6px solid #f59e0b; }
.safe { border-left: 6px solid #16a34a; }
.small {
    font-size: 14px;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR (NO UPLOAD HERE)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚖️ CARA-Bot")
    st.caption("AI Contract Risk Analyzer for SMEs")
    st.divider()
    st.success(
        "🔒 Privacy First\n\n"
        "• Files never leave your system\n"
        "• No cloud storage\n"
        "• LLM used only for explanations"
    )

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------
st.markdown("<h1>CARA-Bot</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Upload a contract, detect risks, and understand legal terms in simple language.</div>",
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# MAIN FILE UPLOAD (CENTER)
# ---------------------------------------------------------
st.markdown("### 📄 Upload Contract")
uploaded_file = st.file_uploader(
    label="Upload Contract",
    type=["pdf", "docx", "txt"],
    label_visibility="collapsed"
)

if not uploaded_file:
    st.markdown("""
    <div class="card" style="text-align:center;">
        <h3>Start by uploading a contract</h3>
        <p class="small">
            Supported formats: PDF, DOCX, TXT<br>
            Best for employment, vendor, and service agreements
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# FILE INGESTION
# ---------------------------------------------------------
os.makedirs("temp", exist_ok=True)
temp_path = os.path.join("temp", uploaded_file.name)

with open(temp_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

with st.spinner("Reading contract…"):
    if uploaded_file.name.endswith(".pdf"):
        raw_text = read_pdf(temp_path)
    elif uploaded_file.name.endswith(".docx"):
        raw_text = read_docx(temp_path)
    else:
        raw_text = uploaded_file.read().decode("utf-8")

clean_txt = clean_text(raw_text)
lang = detect_language_code(clean_txt)

st.markdown(f"**File:** `{uploaded_file.name}` &nbsp;&nbsp;|&nbsp;&nbsp; **Language:** `{lang.upper()}`")

analyze_btn = st.button("🚀 Analyze Contract", type="primary")

# ---------------------------------------------------------
# ANALYSIS PIPELINE
# ---------------------------------------------------------
if analyze_btn:
    with st.spinner("Analyzing contract…"):
        contract_type_info = classify_contract_type(clean_txt)
        clauses = extract_clauses_from_text(clean_txt)

        rules_path = os.path.join(os.path.dirname(__file__), "..", "risk_engine", "risk_rules.yaml")
        risk_rules = load_risk_rules(rules_path)

        analyzed_clauses, all_risks = [], []

        for clause in clauses:
            scores = classify_clause_rule_based(clause["text"])
            label = max(scores, key=scores.get) if scores else "General"
            intents = detect_clause_intent(clause["text"])
            risks = evaluate_risk(clause["text"], label, risk_rules)

            if risks:
                all_risks.extend(risks)

            analyzed_clauses.append({
                "id": clause["clause_id"],
                "text": clause["text"],
                "label": label,
                "intents": intents,
                "risks": risks
            })

        st.session_state["analysis"] = {
            "type": contract_type_info,
            "clauses": clauses,
            "analyzed": analyzed_clauses,
            "risks": all_risks,
            "text": clean_txt
        }

# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------
if "analysis" in st.session_state:
    data = st.session_state["analysis"]

    st.markdown("### 📊 Contract Overview")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"<div class='card metric'><h3>Type</h3><p>{data['type']['contract_type']}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card metric'><h3>Confidence</h3><p>{data['type']['confidence']*100:.0f}%</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card metric'><h3>Clauses</h3><p>{len(data['clauses'])}</p></div>", unsafe_allow_html=True)
    with c4:
        color = "#dc2626" if data["risks"] else "#16a34a"
        st.markdown(f"<div class='card metric'><h3>Risks</h3><p style='color:{color}'>{len(data['risks'])}</p></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # DOWNLOAD PDF (CLEAR & VISIBLE)
    # -----------------------------------------------------
    st.markdown("### 📥 Export Risk Report")

    report_path = os.path.join("temp", "CARA_Bot_Risk_Report.pdf")
    generate_pdf_report({
        "contract_type": data["type"]["contract_type"],
        "confidence": data["type"]["confidence"],
        "risks": data["risks"]
    }, report_path)

    with open(report_path, "rb") as f:
        st.download_button(
            label="📥 Download Risk Report (PDF)",
            data=f.read(),
            file_name="CARA_Bot_Risk_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------
    risk_tab, clause_tab, text_tab = st.tabs(["⚠️ Risks", "📝 Clauses", "📄 Full Text"])

    with risk_tab:
        if not data["risks"]:
            st.success("No major risks detected.")
        else:
            for i, risk in enumerate(data["risks"]):
                level = "high" if risk["severity"] in ["High", "Critical"] else "medium"
                # Check for existing explanation
                explanation = risk.get("explanation")
                
                st.markdown(f"""
                <div class="risk-card {level}">
                    <h4>⚠ {risk['risk_id']} ({risk['severity']})</h4>
                    <p><b>Reason:</b> {risk['reason']}</p>
                    <p class="small">{risk['clause_text']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if explanation:
                     st.info(f"💡 Explanation: {explanation['plain_explanation']}")
                     st.caption(f"Suggestion: {explanation['suggested_alternative']}")

                if st.button("🤖 Explain in simple language", key=f"exp_{i}"):
                    with st.spinner("Generating explanation…"):
                        expl = generate_clause_explanation(risk["clause_text"], risk)
                        # Store in session state persistence
                        data["risks"][i]["explanation"] = expl
                        st.rerun()

    with clause_tab:
        for c in data["analyzed"]:
            with st.expander(f"Clause {c['id']} • {c['label']}"):
                st.write(c["text"])
                st.caption(f"Intent: {', '.join(c['intents']) or 'N/A'}")

    with text_tab:
        st.text_area("Contract Text", data["text"], height=600)
