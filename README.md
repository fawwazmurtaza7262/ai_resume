# Smart Resume Analyzer

Upload a resume (PDF or TXT) and paste a job description to get:
- **Match Score** — TF-IDF cosine similarity + skill-gap weighted composite
- **Missing Skills** — compared against a curated 80+ skill dictionary
- **Improvement Suggestions** — tailored, actionable tips
- **Downloadable Report** — plain-text export

## Setup

```bash
cd resume_analyzer
pip install -r requirements.txt
python -m nltk.downloader stopwords wordnet punkt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| NLP | NLTK (lemmatization, stopwords) |
| Similarity | scikit-learn TF-IDF + cosine similarity |
| PDF parsing | pypdf / pdfplumber |

## How scoring works

```
score = 0.55 × TF-IDF_cosine_similarity + 0.45 × skill_match_ratio
```

- **TF-IDF similarity** captures semantic overlap via bigram vectors
- **Skill match ratio** measures how many job-required skills appear in the resume
