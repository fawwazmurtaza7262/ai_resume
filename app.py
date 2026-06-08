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