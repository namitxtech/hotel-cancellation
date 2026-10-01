# Skill Gap Analyzer

Tell it your skills (or upload a resume) and pick a target role. It shows your match score,
the skills the market expects that you're missing, and a prioritized learning roadmap.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py`: Streamlit UI
- `parser.py`: PDF/DOCX/TXT reading and skill detection
- `analyzer.py`: scoring, category balance, roadmap
- `skills_data.py`: skill catalog and 10 role profiles (edit this to add roles or skills)
