# 🔍 FactLens — AI Fact Checking Web App
> Upload any PDF → Gemini AI extracts claims → Tavily searches live web → Verdict report

Built for **CogCulture Assessment** (Management Trainee - Product Management)

**✅ 100% FREE — No credit card needed**

---

## 🚀 Live Demo
**Deployed App:** [your-app.streamlit.app](https://your-app.streamlit.app)

---

## ✨ What It Does

1. 📄 **Upload PDF** — any marketing deck, report, whitepaper
2. 🧠 **Gemini AI** extracts all verifiable claims (stats, dates, figures)
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
| AI / LLM | Google Gemini 1.5 Flash | **Free** (1500 req/day) |
| Web Search | Tavily API | **Free** (1000 searches/month) |
| PDF Parsing | pdfplumber | Free |
| Hosting | Streamlit Cloud | **Free** |

---

## 🔑 Get Your Free API Keys

### Gemini API (Google AI Studio) — FREE
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API Key"**
4. Copy the key (starts with `AIza...`)

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
GEMINI_API_KEY = "AIza..."
TAVILY_API_KEY = "tvly-..."
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

Made with ❤️ for CogCulture | [cogculture.agency](https://cogculture.agency)
