// Node.js + Express: serves the dashboard, exposes results from the Python/SQL pipeline,
// and calls the Python prediction function through a child process.
const express = require("express");
const { execFile } = require("child_process");
const fs = require("fs");
const path = require("path");
const app = express();
const PY = process.env.PYTHON || "python3";
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));
app.use("/vendor", express.static(path.join(__dirname, "node_modules/chart.js/dist")));

app.get("/api/results", (req, res) => {
  const f = path.join(__dirname, "output/results.json");
  if (!fs.existsSync(f)) return res.status(404).json({ error: "Run `python3 pipeline.py` first." });
  res.json(JSON.parse(fs.readFileSync(f, "utf8")));
});

app.post("/api/predict", (req, res) => {
  const b = req.body, need = ["lead_time", "adr", "total_nights", "hotel", "deposit_type", "market_segment"];
  const missing = need.filter(k => b[k] === undefined || b[k] === "");
  if (missing.length) return res.status(400).json({ error: "Missing: " + missing.join(", ") });
  execFile(PY, ["predict.py", JSON.stringify(b)], { cwd: __dirname }, (err, out, stderr) => {
    if (err) return res.status(500).json({ error: "Python failed", detail: stderr });
    res.json(JSON.parse(out));
  });
});

app.post("/api/refresh", (req, res) => {   // re-runs the whole Python pipeline
  execFile(PY, ["pipeline.py"], { cwd: __dirname }, (err, out, stderr) =>
    err ? res.status(500).json({ error: stderr }) : res.json({ ok: true }));
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Dashboard running at http://localhost:${port}`));
