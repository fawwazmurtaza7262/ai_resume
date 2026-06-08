import streamlit as st
import re
import io
from analyzer import ResumeAnalyzer

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom css ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

.stApp { background-color: #0d0d0d; }
 
h1, h2, h3 {
    font-family: 'Space Mono', monospace;
}

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;  
}

.hero-sub{
    color: #888;
    font-size: 1rem;
    font-family: 'space mono', monospace;
    margin-bottom: 2rem;
}

metric-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
 
.score-ring {
    font-family: 'Space Mono', monospace;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
}
 
.score-label {
    color: #888;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.4rem;
}
 
.skill-chip {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-family: 'Space Mono', monospace;
    margin: 0.2rem;
}
 
.chip-found {
    background: #0d2e1e;
    border: 1px solid #00ff88;
    color: #00ff88;
}
 
.chip-missing {
    background: #2e0d0d;
    border: 1px solid #ff4d4d;
    color: #ff4d4d;
}
 
.suggestion-card {
    background: #161616;
    border-left: 3px solid #00c4ff;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.93rem;
    line-height: 1.6;
}
 
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #555;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #222;
}
 
div[data-testid="stFileUploader"] {
    background: #111;
    border: 1.5px dashed #333;
    border-radius: 10px;
    padding: 0.5rem;
}
 
div[data-testid="stTextArea"] textarea {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}
 
.stButton > button {
    background: linear-gradient(135deg, #00ff88, #00c4ff);
    color: #000;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 0.9rem;
    border: none;
    border-radius: 8px;
    padding: 0.7rem 2rem;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
}
 
.stButton > button:hover { opacity: 0.85; }
 
.stProgress > div > div {
    background: linear-gradient(90deg, #00ff88, #00c4ff);
    border-radius: 4px;
}
 
.divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True) 

# Headers
st.markdown("<h1 class='hero-title'>Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>// match · analyze · optimize</div>", unsafe_allow_html=True) 
analyzer = ResumeAnalyzer()

# Input columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-header">01 — Resume</div>', unsafe_allow_html=True)
    upload = st.file_uploader("Upload resume (.pdf or .txt)", type=["pdf", "txt"], label_visibility="collapsed")
    resume_text = ""
    if upload:
        if upload.type == "application/pdf":
            resume_text = analyzer.extract_pdf(upload.read())
        else:
            resume_text = upload.read().decode("utf-8", errors="ignore")
        st.success(f"✓  {upload.name}  ({len(resume_text.split())} words)")
 
with col2:
    st.markdown('<div class="section-header">02 — Job Description</div>', unsafe_allow_html=True)
    job_text = st.text_area(
        "Paste job description",
        height=200,
        placeholder="Paste the full job description here…",
        label_visibility="collapsed"
    )
 
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Analyze button ─────────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([2, 2, 2])
with btn_col:
    analyze = st.button("Analyze Match →")
 
# ── Results ───────────────────────────────────────────────────────────────────
if analyze:
    if not resume_text:
        st.error("Please upload a resume first.")
    elif not job_text.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing…"):
            results = analyzer.analyze(resume_text, job_text)
 
        score = results["score"]
        found_skills = results["found_skills"]
        missing_skills = results["missing_skills"]
        suggestions = results["suggestions"]
        keyword_coverage = results["keyword_coverage"]
 
        # Score color
        if score >= 75:
            score_color = "#00ff88"
        elif score >= 50:
            score_color = "#ffd700"
        else:
            score_color = "#ff4d4d"
 
        # ── Top metrics row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="score-ring" style="color:{score_color}">{score}%</div>
                <div class="score-label">Match Score</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="score-ring" style="color:#00c4ff">{len(found_skills)}</div>
                <div class="score-label">Skills Matched</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="score-ring" style="color:#ff4d4d">{len(missing_skills)}</div>
                <div class="score-label">Skills Missing</div>
            </div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="score-ring" style="color:#ffd700">{keyword_coverage}%</div>
                <div class="score-label">Keyword Coverage</div>
            </div>""", unsafe_allow_html=True)
 
        st.markdown('<br>', unsafe_allow_html=True)
        st.progress(score / 100)
 
        # ── Skills breakdown
        sc1, sc2 = st.columns(2, gap="large")
        with sc1:
            st.markdown('<div class="section-header">✓ Skills Found in Resume</div>', unsafe_allow_html=True)
            if found_skills:
                chips = "".join(f'<span class="skill-chip chip-found">{s}</span>' for s in sorted(found_skills))
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:#555">No matching skills detected.</span>', unsafe_allow_html=True)
 
        with sc2:
            st.markdown('<div class="section-header">✗ Skills Missing from Resume</div>', unsafe_allow_html=True)
            if missing_skills:
                chips = "".join(f'<span class="skill-chip chip-missing">{s}</span>' for s in sorted(missing_skills))
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:#555">No critical skills missing!</span>', unsafe_allow_html=True)
 
        # ── Suggestions
        st.markdown('<div class="section-header">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
        for tip in suggestions:
            st.markdown(f'<div class="suggestion-card">{tip}</div>', unsafe_allow_html=True)
 
        # ── Download report
        st.markdown('<div class="section-header">Export</div>', unsafe_allow_html=True)
        report = analyzer.build_report(score, found_skills, missing_skills, suggestions, keyword_coverage)
        st.download_button(
            "⬇  Download Report (.txt)",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )
 
 