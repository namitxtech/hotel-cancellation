"use client";
import { useEffect, useMemo, useState } from "react";
import catalog from "../lib/catalog.json";
import { Radar, Ring } from "../components/Charts";

type Step = { skill: string; priority: string; weeks: number; resource: string };
type Result = {
  score: number; verdict: string; matched: string[]; missing: string[]; have: string[]; weeks: number;
  by_category: Record<string, number>; roadmap: Step[]; reqs: Record<string, number>;
  ranking: { role: string; score: number }[];
};

const ROLES = catalog.roles as Record<string, { desc: string }>;
const SKILLS = Object.keys(catalog.skills).sort();
const COLORS: Record<string, string> = { Critical: "#D93636", Important: "#E8710A", "Nice to have": "#7A869F" };
const TABS = [["gap", "Gap breakdown"], ["balance", "Skill balance"], ["road", "Learning roadmap"], ["roles", "Other roles"]];

export default function Home() {
  const [role, setRole] = useState("Data Scientist");
  const [picked, setPicked] = useState<string[]>([]);
  const [typed, setTyped] = useState("");
  const [resume, setResume] = useState<{ name: string; skills: string[] } | null>(null);
  const [q, setQ] = useState("");
  const [tab, setTab] = useState("gap");
  const [res, setRes] = useState<Result | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [drag, setDrag] = useState(false);

  const skills = useMemo(() => Array.from(new Set([...picked, ...(resume?.skills ?? [])])), [picked, resume]);
  const hasInput = skills.length > 0 || typed.trim().length > 0;

  // Live analysis: every change is sent to the Python function (debounced).
  useEffect(() => {
    if (!hasInput) { setRes(null); return; }
    const ac = new AbortController();
    const t = setTimeout(async () => {
      setBusy(true); setErr("");
      try {
        const r = await fetch("/api/analyze", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ role, skills, text: typed }), signal: ac.signal,
        });
        const d = await r.json();
        if (!r.ok) throw new Error(d.error || r.statusText);
        setRes(d);
      } catch (e: any) { if (e.name !== "AbortError") setErr(e.message); }
      finally { if (!ac.signal.aborted) setBusy(false); }
    }, 300);
    return () => { clearTimeout(t); ac.abort(); };
  }, [role, skills, typed, hasInput]);

  async function upload(f?: File) {
    if (!f) return;
    if (f.size > 4_000_000) { setErr("That file is over 4 MB. Please upload a smaller export."); return; }
    setBusy(true); setErr("");
    try {
      const r = await fetch(`/api/parse?filename=${encodeURIComponent(f.name)}`, { method: "POST", body: f });
      const d = await r.json();
      if (!r.ok) throw new Error(d.error);
      setResume({ name: f.name, skills: d.skills });
      if (!d.chars) setErr("No text found. Scanned PDFs need to be exported as text-based PDFs.");
      else if (!d.skills.length) setErr("Read the file, but found no skills from our catalog.");
    } catch (e: any) { setErr(e.message); }
    finally { setBusy(false); }
  }

  const toggle = (s: string) => setPicked((p) => (p.includes(s) ? p.filter((x) => x !== s) : [...p, s]));
  const shown = SKILLS.filter((s) => s.toLowerCase().includes(q.toLowerCase()));
  const extra = res ? res.have.filter((s) => !(s in res.reqs)) : [];

  return (
    <div className="layout">
      <aside className="side">
        <h2 className="display">🧭 Skill Gap Analyzer</h2>
        <div>
          <label htmlFor="role">Target role</label>
          <select id="role" value={role} onChange={(e) => setRole(e.target.value)}>
            {Object.keys(ROLES).map((r) => <option key={r}>{r}</option>)}
          </select>
          <small>{ROLES[role].desc}</small>
        </div>

        <div>
          <span className="lbl">Upload your resume</span>
          <label className={`drop ${drag ? "on" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); upload(e.dataTransfer.files[0]); }}>
            <input type="file" accept=".pdf,.docx,.txt" onChange={(e) => upload(e.target.files?.[0])} />
            {resume ? `📄 ${resume.name}` : "Drop a PDF, DOCX or TXT here, or click to browse"}
          </label>
          {resume?.skills.map((s) => (
            <button key={s} className="chip have" onClick={() => setResume({ ...resume, skills: resume.skills.filter((x) => x !== s) })}
              aria-label={`Remove ${s} found in resume`}>{s} ×</button>
          ))}
        </div>

        <div>
          <label htmlFor="q">Pick skills you know</label>
          <input id="q" type="search" placeholder="Search skills…" value={q} onChange={(e) => setQ(e.target.value)} />
          <div className="picker">
            {shown.map((s) => <button key={s} className="chip" aria-pressed={picked.includes(s)} onClick={() => toggle(s)}>{s}</button>)}
          </div>
        </div>

        <div>
          <label htmlFor="typed">Or type them</label>
          <textarea id="typed" rows={3} value={typed} onChange={(e) => setTyped(e.target.value)}
            placeholder="e.g. python, sql, power bi, docker, communication" />
        </div>
        {err && <div className="err" role="alert">{err}</div>}
      </aside>

      <main className={`main ${busy ? "busy" : ""}`}>
        {!res ? (
          <section className="hero"><div>
            <h1>See exactly which skills stand between you and your next role.</h1>
            <p>Upload your resume or list what you know in the sidebar. You&apos;ll get a match score, the missing skills ranked by market demand, and a learning roadmap.</p>
          </div></section>
        ) : (<>
          <section className="hero">
            <div><h1>You match {res.score}% of what {role} roles ask for.</h1><p>{res.verdict}</p></div>
            <Ring score={res.score} />
          </section>
          <div className="stats">
            <div className="stat"><b style={{ color: "var(--teal)" }}>{res.matched.length}</b><span>required skills you have</span></div>
            <div className="stat"><b style={{ color: "var(--orange)" }}>{res.missing.length}</b><span>skills still missing</span></div>
            <div className="stat"><b>~{res.weeks} weeks</b><span>to close the gap, one skill at a time</span></div>
          </div>

          <div className="tabs" role="tablist">
            {TABS.map(([id, label]) => (
              <button key={id} role="tab" aria-selected={tab === id} onClick={() => setTab(id)}>{label}</button>
            ))}
          </div>

          {tab === "gap" && (<>
            <div className="cols">
              <div><h3>Skills you have</h3>
                {res.matched.map((s) => <span key={s} className="chip have">{s}</span>)}
                {!res.matched.length && <p className="muted">None of the required skills yet.</p>}</div>
              <div><h3>Skills to learn</h3>
                {res.missing.map((s) => <span key={s} className="chip gap">{s}</span>)}
                {!res.missing.length && <p className="muted">No gaps. You cover everything.</p>}</div>
            </div>
            {extra.length > 0 && <><h3 style={{ margin: "1.2rem 0 .3rem" }}>Other skills you listed</h3>
              <p className="muted">Not required for this role, but they still count on a resume. {extra.join(", ")}</p></>}
          </>)}

          {tab === "balance" && (<>
            <Radar data={res.by_category} />
            <p className="muted">Each axis shows how much of the role&apos;s demand in that area you already cover.</p>
          </>)}

          {tab === "road" && (res.roadmap.length === 0
            ? <p>Nothing left to learn for this role. Build a portfolio project and start applying.</p>
            : <>
              <p className="muted">Ordered by market demand first, then by how quickly you can learn each skill. Already know one? Mark it and watch your score update.</p>
              {res.roadmap.map((r) => (
                <div key={r.skill} className="step" style={{ "--c": COLORS[r.priority] } as React.CSSProperties}>
                  <div><div className="t">{r.skill}<em>{r.priority}</em></div>
                  <div className="m">About {r.weeks} weeks · {r.resource}</div></div>
                  <button className="know" onClick={() => toggle(r.skill)}>I know this</button>
                </div>
              ))}
            </>)}

          {tab === "roles" && (<>
            {res.ranking.map((r) => (
              <button key={r.role} className={`bar ${r.role === role ? "cur" : ""}`} onClick={() => setRole(r.role)}>
                <span>{r.role}</span>
                <span className="track"><span className="fill" style={{ width: `${r.score}%`, display: "block" }} /></span>
                <span>{r.score}%</span>
              </button>
            ))}
            <p className="muted">Your best fit right now: <b>{res.ranking[0].role}</b> ({res.ranking[0].score}%). Click any role to analyze it.</p>
          </>)}
        </>)}
      </main>
    </div>
  );
}
