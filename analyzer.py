"""
analyzer.py  –  Core NLP engine for the Smart Resume Analyzer
Uses: scikit-learn TF-IDF, NLTK, and a curated tech-skills dictionary.
"""
 
from __future__ import annotations
import re
import io
import math
from typing import TypedDict
 
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
 
 
# ── NLTK bootstrap ────────────────────────────────────────────────────────────
for pkg in  ("stopwords", "wordnet", "punkt", "punkt_tab", "omw-1.4"):
    try:
        nltk.data.find(f"corpora/{pkg}")
    except LookupError:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass
        
# ── Skill dictionary ────────────────────────────────────────────────────────────
SKILL_KEYWORDS: set[str] = {
    # Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "bash", "shell",
    "perl", "haskell", "lua", "dart", "elixir",
    # Web / Frontend
    "html", "css", "react", "angular", "vue", "nextjs", "nuxtjs", "svelte",
    "jquery", "bootstrap", "tailwind", "webpack", "vite", "graphql", "rest",
    "restful", "api",
    # Backend / Frameworks
    "node", "nodejs", "express", "django", "flask", "fastapi", "spring", "rails",
    "laravel", "asp.net", "dotnet", ".net",
    # Data / ML / AI
    "sql", "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis",
    "elasticsearch", "nosql", "cassandra", "dynamodb", "firebase",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas",
    "numpy", "scipy", "matplotlib", "seaborn", "plotly", "tableau", "power bi",
    "spark", "hadoop", "hive", "kafka", "airflow", "dbt",
    # Cloud / DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "jenkins", "github actions", "ci/cd", "cicd",
    "linux", "unix", "nginx", "apache",
    # Version Control / Tools
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "agile", "scrum", "kanban",
    # Soft / General
    "communication", "leadership", "teamwork", "problem solving",
    "analytical", "collaboration", "project management", "time management",
}

# ── Result type ───────────────────────────────────────────────────────────────
class AnalysisResult(TypedDict):
    score: int
    keyword_coverage: int
    found_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
 
 
class ResumeAnalyzer:
    def __init__(self) -> None:
        self._lemmatizer = WordNetLemmatizer()
        try:
            self._stop = set(stopwords.words("english"))
        except Exception:
            self._stop = set()
            
 # ── Public API ─────────────────────────────────────────────────────────────
def extract_pdf(self, pdf_bytes: bytes) -> str:
    """Extract text from a PDF file (bytes)."""
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except ImportError:
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        except ImportError:
            return ""
        
def analyze(self, resume: str, job: str) -> AnalysisResult:
    resume_clean = self._preprocess(resume)
    job_clean = self.preprocess(job)
    
    tfidf_score = self._tfidf_similarity(resume_clean, job_clean)
    found, missing = self._skill_gap(resume_clean, job_clean)
    skill_ratio = len(found) / max(len(found) + len(missing), 1)
    
    # weighted composite score
    raw = 0.55 * tfidf_score + 0.45 * skill_ratio
    score = min(100, math.cell(raw * 100))
    
    keyword_coverage = self._keyword_coverage(resume_clean, job_clean)
    suggestions = self._generate_suggestions(score, found, missing, resume, job)
 
    return AnalysisResult(
        score=score,
        keyword_coverage=keyword_coverage,
        found_skills=list(found),
        missing_skills=list(missing),
        suggestions=suggestions,
    )
    
    def build_report(
        self,
        score: int,
        found: list[str],
        missing: list[str],
        suggestions: list[str],
        coverage: int,
    ) -> str:
        lines = [
            "=" * 60,
            "  SMART RESUME ANALYZER — REPORT",
            "=" * 60,
            f"\nMatch Score        : {score}%",
            f"Keyword Coverage   : {coverage}%",
            f"Skills Found       : {len(found)}",
            f"Skills Missing     : {len(missing)}",
            "\n── MATCHED SKILLS ──────────────────────────────",
            ", ".join(sorted(found)) if found else "(none detected)",
            "\n── MISSING SKILLS ──────────────────────────────",
            ", ".join(sorted(missing)) if missing else "(none — great match!)",
            "\n── IMPROVEMENT SUGGESTIONS ──────────────────────",
        ]
        for i, s in enumerate(suggestions, 1):
            lines.append(f"{i}. {s}")
        lines += ["\n" + "=" * 60]
        return "\n".join(lines)
        