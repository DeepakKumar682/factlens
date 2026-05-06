# 🔍 FactLens — AI Fact Checking Web App
> Upload any PDF → AI extracts claims → Tavily searches live web → Verdict report

Built for **CogCulture Assessment** (Management Trainee - Product Management)

**✅ 100% FREE — No credit card needed**

---

## 🚀 Live Demo
**Deployed App:** [factlens-ai.streamlit.app](https://factlens-ai.streamlit.app)

---

## ✨ What It Does

1. 📄 **Upload PDF** — any marketing deck, report, whitepaper
2. 🧠 **Groq AI (LLaMA 3.3)** extracts all verifiable claims (stats, dates, figures)
3. 🌐 **Tavily Search** cross-references each claim against live web
4. 📊 **Verdict Report** — every claim flagged as:
   - ✅ **Verified** — matches web evidence
   - ⚠️ **Inaccurate** — outdated or partially wrong (with correction)
   - ❌ **False** — no supporting evidence found

---

## 🛠️ Tech Stack

| Layer | Tool | Cost |
|-------|------|------|
| Frontend | Streamlit | Free |
| AI / LLM | Groq + LLaMA 3.3 70B | **Free** (generous daily limit) |
| Web Search | Tavily API | **Free** (1000 searches/month) |
| PDF Parsing | pdfplumber | Free |
| Hosting | Streamlit Cloud | **Free** |

---

## 🔑 Get Your Free API Keys

### Groq API — FREE
1. Go to [console.groq.com](https://console.groq.com)
2. Sign in with Google
3. Click **"API Keys"** → **"Create API Key"**
4. Copy the key (starts with `gsk_...`)

### Tavily Search API — FREE
1. Go to [tavily.com](https://tavily.com)
2. Sign up with email
3. Go to Dashboard → Copy your API key (starts with `tvly-...`)

---

## ⚙️ Local Setup

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/factlens
cd factlens

# 2. Install
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Enter your API keys in the sidebar when the app opens.

---

## 🌐 Deploy FREE on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. **New app** → Select repo → Main file: `app.py`
4. Click **Advanced settings** → Add secrets:
```toml
GEMINI_API_KEY = "gsk_your_groq_key_here"
TAVILY_API_KEY = "tvly-your_tavily_key_here"
```
5. **Deploy** → Live URL in ~2 minutes ✅

---

## 📁 Project Structure

```
factlens/
├── app.py              ← Streamlit app (all logic)
├── requirements.txt    ← 3 dependencies only
├── README.md           ← This file
└── .gitignore          ← Keeps secrets safe
```

---

## 🧠 How It Works

```
User uploads PDF
      ↓
pdfplumber extracts all text
      ↓
Groq AI (LLaMA 3.3) identifies all verifiable claims
      ↓
For each claim → Tavily searches the live web
      ↓
Groq cross-references claim vs web evidence → Verdict
      ↓
Report with verdicts, explanations, and source links
```

---

Made with CogCulture❤️
