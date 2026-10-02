"""POST /api/parse?filename=cv.pdf  (raw file bytes)  ->  skills found in the resume."""
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from _util import read_body, send_json
from core.parser import extract_skills, read_resume


class _Upload:
    def __init__(self, name, data):
        self.name, self._data = name, data

    def getvalue(self):
        return self._data


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            name = parse_qs(urlparse(self.path).query).get("filename", ["resume.txt"])[0]
            text = read_resume(_Upload(name, read_body(self)))
            send_json(self, 200, {"skills": sorted(extract_skills(text)), "chars": len(text.strip())})
        except Exception as exc:
            send_json(self, 400, {"error": f"Could not read this file ({exc}). Try a PDF, DOCX or TXT export."})
