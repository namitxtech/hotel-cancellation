# Skill Gap Analyzer (Next.js + Python)

Pick a target role, upload a resume or list your skills, and get a match score, the skills you're
missing, and a prioritized learning roadmap.

**Stack:** Next.js 15 (React, TypeScript) UI, Python serverless functions for all analysis, deployed on Vercel.

```
app/ components/ lib/      Next.js UI (lib/catalog.json is generated from the Python data)
api/analyze.py             POST /api/analyze  -> score, gaps, roadmap, role ranking
api/parse.py               POST /api/parse    -> resume (PDF/DOCX/TXT) -> detected skills
core/                      Your original Python logic: skills_data.py, analyzer.py, parser.py
```

## Deploy to Vercel
1. Push this folder to a GitHub repo.
2. vercel.com > Add New > Project > import the repo. Framework is detected as Next.js. Click Deploy.
   (Or: `npm i -g vercel && vercel --prod`.) `requirements.txt` is installed automatically for `api/*.py`.

## Run locally
```bash
npm install
npx vercel dev   # runs Next.js + the Python functions together (first run asks you to log in/link)
```

## Edit skills or roles
Change `core/skills_data.py`, then run `npm run sync-catalog` to refresh `lib/catalog.json`.

## Notes
- Resume uploads are limited to 4 MB (Vercel's request limit). Scanned/image-only PDFs have no text to read.
- Resumes are processed in memory and never stored.
