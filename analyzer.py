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
    
 # ── Private helpers ────────────────────────────────────────────────────────
    def _preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in self._stop and len(t) > 1]
        try:
            tokens = [self._lemmatizer.lemmatize(t) for t in tokens]
        except Exception:
            pass
        return " ".join(tokens)
    
    def _tfidf_similarity(self, resume: str, job: str) -> float:
        try:
            vec = TfidfVectorizer(ngram_range=(1,2))
            tfidf = vectorizer.fit_transform([resume, job])
            return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        except Exception:
            return 0.0
    
    def _skill_gap(self, resume_raw: str, job_raw: str) -> tuple[set[str], set[str]]:
        """Return (found_skills, missing_skills) using multi-word matching."""
        job_skills: set[str] = set()
        for skill in SKILL_KEYWORDS:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, job_raw):
                job_skills.add(skill)
 
        found: set[str] = set()
        missing: set[str] = set()
        for skill in job_skills:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, resume_raw):
                found.add(skill)
            else:
                missing.add(skill)
 
        return found, missing
 
    def _keyword_coverage(self, resume_clean: str, job_clean: str) -> int:
        job_words = set(job_clean.split())
        resume_words = set(resume_clean.split())
        if not job_words:
            return 0
        overlap = job_words & resume_words
        return min(100, round(len(overlap) / len(job_words) * 100))
 
    def _generate_suggestions(
        self,
        score: int,
        found: set[str],
        missing: set[str],
        resume_raw: str,
        job_raw: str,
    ) -> list[str]:
        tips: list[str] = []
 
        # Skill-based tips
        if missing:
            top_missing = sorted(missing)[:6]
            tips.append(
                f"Add the following missing skills to your resume (or a skills section): "
                f"{', '.join(top_missing)}."
            )
 
        # Score-based tips
        if score < 40:
            tips.append(
                "Your overall match is low. Consider tailoring your resume "
                "more closely to this specific role by mirroring the job description's language."
            )
        elif score < 65:
            tips.append(
                "Your match is moderate. Strengthen alignment by incorporating "
                "more of the job's key phrases into your bullet points."
            )
        else:
            tips.append(
                "Strong match! Fine-tune your summary section to directly echo "
                "the job's top-priority requirements."
            )
 
        # Quantification check
        numbers = re.findall(r"\b\d+[%x]?\b", resume_raw)
        if len(numbers) < 3:
            tips.append(
                "Quantify your achievements — recruiters respond to metrics. "
                "E.g. 'Reduced load time by 40%' or 'Managed a team of 8 engineers'."
            )
 
        # Resume length check
        word_count = len(resume_raw.split())
        if word_count < 250:
            tips.append(
                "Your resume appears short. Expand your experience bullets with "
                "action verbs, tools used, and measurable outcomes."
            )
        elif word_count > 900:
            tips.append(
                "Your resume is quite long. Aim for one page (≈400–600 words) "
                "for <10 years of experience to keep recruiters engaged."
            )
 
        # Action verbs check
        action_verbs = {
            "built", "developed", "led", "designed", "implemented", "improved",
            "reduced", "increased", "created", "managed", "optimized", "deployed",
        }
        resume_lower = resume_raw.lower()
        used_verbs = action_verbs & set(resume_lower.split())
        if len(used_verbs) < 3:
            tips.append(
                "Use strong action verbs at the start of bullet points: "
                "Built, Designed, Optimized, Led, Deployed, etc."
            )
 
        # Summary check
        has_summary = any(w in resume_lower for w in ["summary", "objective", "profile", "about"])
        if not has_summary:
            tips.append(
                "Add a 2–3 sentence professional summary at the top of your resume "
                "that directly targets this role."
            )
 
        # Certifications
        if "certified" not in resume_lower and "certification" not in resume_lower:
            relevant_certs = [s for s in missing if s in ("aws", "azure", "gcp", "kubernetes", "docker")]
            if relevant_certs:
                tips.append(
                    f"Consider earning a certification in {relevant_certs[0].upper()} — "
                    "it can significantly boost your candidacy for this role."
                )
 
    return tips
        