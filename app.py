import streamlit as st
import pdfplumber
import requests
import json
import time
import io
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FactLens — AI Fact Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    font-family: 'DM Mono', monospace;
    color: #e8e4dc;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0a0a0f;
    padding: 2rem 3rem;
}

[data-testid="stHeader"] { background: transparent !important; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    background: linear-gradient(135deg, #f0e6c8 0%, #c8a96e 50%, #f0e6c8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    font-weight: 300;
    color: #6b6660;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 3rem;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #c8a96e33, transparent);
    margin: 2rem 0;
}

[data-testid="stFileUploader"] {
    background: #12121a !important;
    border: 1px dashed #c8a96e44 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}

[data-testid="stFileUploader"] label {
    color: #c8a96e !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stTextInput"] input {
    background: #12121a !important;
    border: 1px solid #ffffff11 !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

[data-testid="stTextInput"] label {
    color: #6b6660 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c8a96e, #a8893e) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px #c8a96e33 !important;
}

.claim-card {
    background: #12121a;
    border: 1px solid #ffffff0d;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s ease;
}

.claim-card:hover { border-color: #ffffff1a; }

.claim-header {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.75rem;
    border-radius: 100px;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
}

.badge-verified   { background: #1a3a2a; color: #4ade80; border: 1px solid #4ade8033; }
.badge-inaccurate { background: #3a2a0a; color: #fbbf24; border: 1px solid #fbbf2433; }
.badge-false      { background: #3a0a0a; color: #f87171; border: 1px solid #f8717133; }

.claim-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    color: #e8e4dc;
    line-height: 1.6;
    flex: 1;
}

.explanation {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #8a8480;
    line-height: 1.7;
    padding-top: 0.75rem;
    border-top: 1px solid #ffffff08;
}

.source-tag {
    display: inline-block;
    background: #1a1a22;
    border: 1px solid #ffffff0d;
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    font-size: 0.7rem;
    color: #c8a96e88;
    margin-top: 0.5rem;
    margin-right: 0.3rem;
    word-break: break-all;
}

.stats-bar {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    background: #12121a;
    border: 1px solid #ffffff0d;
    border-radius: 12px;
}

.stat-item { text-align: center; flex: 1; }
.stat-num  { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; }
.stat-label { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6b6660; }

.text-green  { color: #4ade80; }
.text-yellow { color: #fbbf24; }
.text-red    { color: #f87171; }
.text-gold   { color: #c8a96e; }

[data-testid="stExpander"] {
    background: #12121a !important;
    border: 1px solid #ffffff0d !important;
    border-radius: 12px !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #c8a96e33; border-radius: 2px; }

.info-box {
    background: #0f1520;
    border: 1px solid #818cf822;
    border-left: 3px solid #818cf8;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.8rem;
    color: #818cf8cc;
    margin: 1rem 0;
    line-height: 1.6;
}

.step-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #1a1a22;
    border: 1px solid #ffffff0d;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.78rem;
    color: #8a8480;
    margin: 0.3rem;
}

.step-pill span { color: #c8a96e; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─── Gemini API Call ─────────────────────────────────────────────────────────

def call_gemini(prompt: str, api_key: str) -> str:
    """Groq API — FREE, fast, no rate limits"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2048,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def safe_parse_json(raw: str):
    """Strip markdown fences and extract JSON from Gemini response."""
    raw = raw.strip().replace("```json", "").replace("```", "").strip()
    # Find first complete JSON structure
    for start_ch, end_ch in [("[", "]"), ("{", "}")]:
        s = raw.find(start_ch)
        e = raw.rfind(end_ch)
        if s != -1 and e > s:
            try:
                return json.loads(raw[s : e + 1])
            except json.JSONDecodeError:
                continue
    return json.loads(raw)  # Last attempt — will raise if truly invalid


# ─── Core Pipeline ───────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes) -> str:
    text = ""
    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text.strip()


def extract_claims(doc_text: str, gemini_key: str) -> list:
    prompt = f"""You are a claim extractor. Read the document and extract ALL specific verifiable factual claims.
Focus on: statistics, percentages, dates, numbers, financial figures, market sizes, company facts, scientific claims.

Return ONLY a valid JSON array — no markdown, no explanation, no code fences.
Format: [{{"id": 1, "claim": "exact claim text", "category": "statistic|date|financial|technical|general"}}]

Document:
{doc_text[:6000]}"""

    raw = call_gemini(prompt, gemini_key)
    return safe_parse_json(raw)


def search_web(claim: str, tavily_key: str) -> dict:
    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_key,
                "query": claim,
                "search_depth": "basic",
                "max_results": 5,
                "include_answer": True,
            },
            timeout=15,
        )
        return r.json()
    except Exception as e:
        return {"error": str(e), "results": []}


def verify_claim(claim: str, search_data: dict, gemini_key: str) -> dict:
    context = ""
    sources = []

    if search_data.get("answer"):
        context += f"Web Summary: {search_data['answer']}\n\n"
    for item in search_data.get("results", [])[:4]:
        context += f"Source: {item.get('url', '')}\n{item.get('content', '')[:400]}\n\n"
        sources.append(item.get("url", ""))

    prompt = f"""You are a professional fact-checker. Analyse the claim against web evidence and return a verdict.

CLAIM: "{claim}"

WEB EVIDENCE:
{context[:3000] if context else "No web results. Use your knowledge to assess accuracy."}

Return ONLY a valid JSON object — no markdown, no code fences:
{{"verdict": "Verified", "confidence": "High", "explanation": "2-3 sentences with specific evidence.", "corrected_fact": null}}

Rules:
- verdict must be exactly: "Verified" | "Inaccurate" | "False"
- Verified = supported by evidence
- Inaccurate = partially wrong or outdated → fill corrected_fact
- False = clearly wrong or no evidence → fill corrected_fact
- corrected_fact = null if Verified"""

    raw = call_gemini(prompt, gemini_key)
    result = safe_parse_json(raw)
    result["sources"] = [s for s in sources if s]
    return result


# ─── UI Layout ───────────────────────────────────────────────────────────────

st.markdown('<div class="hero-title">FactLens</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">AI-Powered Claim Verification · Gemini + Tavily · 100% Free</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown('<div class="step-pill"><span>01</span> Upload PDF</div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="step-pill"><span>02</span> Gemini AI extracts claims</div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="step-pill"><span>03</span> Tavily live web search</div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="step-pill"><span>04</span> Verdict report</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Sidebar: API Keys ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ API Keys")
    st.markdown("""
    <div style='background:#1a3a1a; border:1px solid #4ade8033; border-radius:8px;
         padding:0.75rem 1rem; font-size:0.75rem; color:#4ade80; margin-bottom:1rem;'>
    ✅ <b>Both APIs are 100% FREE</b><br>No credit card needed.
    </div>
    """, unsafe_allow_html=True)

    gemini_key = st.text_input(
        "Google Gemini API Key 🆓",
        type="password",
        placeholder="AIza...",
        help="Get free at aistudio.google.com → 1500 req/day free",
    )
    tavily_key = st.text_input(
        "Tavily Search API Key 🆓",
        type="password",
        placeholder="tvly-...",
        help="Get free at tavily.com → 1000 searches/month",
    )

    st.markdown("""
    <div style='font-size:0.72rem; color:#6b6660; line-height:1.9; margin-top:1rem;'>
    <b>Get Gemini key (Free):</b><br>
    1. Go to aistudio.google.com<br>
    2. Sign in with Google<br>
    3. Click "Get API Key"<br>
    4. Create API Key → Copy it<br><br>
    <b>Get Tavily key (Free):</b><br>
    1. Go to tavily.com<br>
    2. Sign up (email)<br>
    3. Dashboard → Copy API key
    </div>
    """, unsafe_allow_html=True)

# Fallback: Streamlit secrets or env vars (for deployment)
if not gemini_key:
    try:
        gemini_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        gemini_key = os.environ.get("GEMINI_API_KEY", "")

if not tavily_key:
    try:
        tavily_key = st.secrets.get("TAVILY_API_KEY", "")
    except Exception:
        tavily_key = os.environ.get("TAVILY_API_KEY", "")

# ─── Main Panel ───────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    uploaded_file = st.file_uploader(
        "Drop your PDF here",
        type=["pdf"],
        help="Works with marketing decks, reports, articles",
    )

with right:
    st.markdown("""
    <div class="info-box">
    📄 Upload any PDF with factual claims.<br><br>
    ⚡ <b>Gemini AI</b> identifies every stat, date, and figure.
    <b>Tavily</b> searches the live web to verify each one.
    Claims are flagged as <b>Verified ✅</b>, <b>Inaccurate ⚠️</b>, or <b>False ❌</b>.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if uploaded_file:
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("🔍 Analyse Document", use_container_width=True)

    if run:
        if not gemini_key:
            st.error("⚠️ Add your Gemini API key in the sidebar. Get it FREE at aistudio.google.com")
            st.stop()
        if not tavily_key:
            st.warning("⚠️ No Tavily key — web search skipped. Add it for better accuracy.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 1. Extract PDF text
        with st.spinner("📄 Reading PDF..."):
            try:
                doc_text = extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
            except Exception as e:
                st.error(f"Could not read PDF: {e}")
                st.stop()

        if not doc_text.strip():
            st.error("PDF appears empty or is a scanned image. Please use a text-based PDF.")
            st.stop()

        with st.expander("📃 Extracted Text Preview"):
            st.text(doc_text[:2000] + ("..." if len(doc_text) > 2000 else ""))

        # 2. Extract claims
        with st.spinner("🧠 Gemini extracting factual claims..."):
            try:
                claims = extract_claims(doc_text, gemini_key)
            except Exception as e:
                st.error(f"Claim extraction failed: {e}")
                st.stop()

        if not claims:
            st.warning("No verifiable claims found in this document.")
            st.stop()

        st.success(f"✅ Found **{len(claims)} verifiable claims**. Verifying now...")
        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Verify each claim
        results = []
        progress_bar = st.progress(0)
        status = st.empty()

        for i, c in enumerate(claims):
            claim_text = c.get("claim", "")
            status.markdown(
                f'<div style="font-size:0.78rem;color:#6b6660;">🔍 Checking {i+1}/{len(claims)}: {claim_text[:80]}...</div>',
                unsafe_allow_html=True,
            )

            search_data = search_web(claim_text, tavily_key) if tavily_key else {}

            try:
                verdict = verify_claim(claim_text, search_data, gemini_key)
                verdict["claim"] = claim_text
                verdict["category"] = c.get("category", "general")
            except Exception as e:
                verdict = {
                    "claim": claim_text,
                    "verdict": "False",
                    "confidence": "Low",
                    "explanation": f"Verification error: {e}",
                    "corrected_fact": None,
                    "sources": [],
                    "category": c.get("category", "general"),
                }

            results.append(verdict)
            progress_bar.progress((i + 1) / len(claims))
            time.sleep(0.5)  # Gemini free tier rate limit

        status.empty()
        progress_bar.empty()

        # 4. Show results
        st.markdown("## 📊 Verification Report")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        verified   = sum(1 for r in results if r["verdict"] == "Verified")
        inaccurate = sum(1 for r in results if r["verdict"] == "Inaccurate")
        false_cnt  = sum(1 for r in results if r["verdict"] == "False")
        total      = len(results)

        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-num text-gold">{total}</div><div class="stat-label">Total Claims</div></div>
            <div class="stat-item"><div class="stat-num text-green">{verified}</div><div class="stat-label">✅ Verified</div></div>
            <div class="stat-item"><div class="stat-num text-yellow">{inaccurate}</div><div class="stat-label">⚠️ Inaccurate</div></div>
            <div class="stat-item"><div class="stat-num text-red">{false_cnt}</div><div class="stat-label">❌ False</div></div>
            <div class="stat-item"><div class="stat-num text-gold">{round(verified/total*100) if total else 0}%</div><div class="stat-label">Accuracy Score</div></div>
        </div>
        """, unsafe_allow_html=True)

        results.sort(key=lambda x: {"False": 0, "Inaccurate": 1, "Verified": 2}.get(x["verdict"], 3))

        for r in results:
            v = r["verdict"]
            badge_cls = {"Verified": "badge-verified", "Inaccurate": "badge-inaccurate", "False": "badge-false"}.get(v, "badge-false")
            icon = {"Verified": "✅", "Inaccurate": "⚠️", "False": "❌"}.get(v, "❓")

            sources_html = "".join(
                f'<a href="{s}" target="_blank" class="source-tag">{s[:55]}...</a>'
                for s in r.get("sources", [])[:3]
            )
            corrected = ""
            if r.get("corrected_fact"):
                corrected = (
                    f'<div style="margin-top:0.75rem;padding:0.75rem;background:#1a120a;'
                    f'border-left:2px solid #fbbf24;border-radius:4px;font-size:0.78rem;color:#fbbf24cc;">'
                    f'<b>✏️ Correct fact:</b> {r["corrected_fact"]}</div>'
                )

            st.markdown(f"""
            <div class="claim-card">
                <div class="claim-header">
                    <div class="badge {badge_cls}">{icon} {v}</div>
                    <div class="claim-text">{r['claim']}</div>
                </div>
                <div class="explanation">
                    {r.get('explanation', '')}
                    {corrected}
                    <div style="margin-top:0.5rem;">{sources_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.72rem;color:#6b6660;text-align:center;">'
            f'FactLens · Powered by Google Gemini + Tavily · {total} claims analysed</div>',
            unsafe_allow_html=True,
        )

else:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem;">
        <div style="font-size:4rem; margin-bottom:1rem; opacity:0.2;">📄</div>
        <div style="font-family:'Syne',sans-serif; font-size:1.1rem; color:#4a4640;">
            Upload a PDF to begin fact-checking
        </div>
        <div style="font-size:0.78rem; color:#3a3830; margin-top:0.5rem;">
            Marketing decks · Research reports · Press releases · Whitepapers
        </div>
    </div>
    """, unsafe_allow_html=True)
