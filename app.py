"""Skill Gap Analyzer: run with `streamlit run app.py`."""
import plotly.graph_objects as go
import streamlit as st

from analyzer import analyze, rank_roles, verdict
from parser import extract_skills, read_resume
from skills_data import CATALOG, ROLES

TEAL, ORANGE, INK = "#0F9D74", "#E8710A", "#1B2338"

st.set_page_config(page_title="Skill Gap Analyzer", page_icon="🧭", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Instrument+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Instrument Sans', sans-serif; }
h1, h2, h3, .display { font-family: 'Bricolage Grotesque', sans-serif !important; letter-spacing: -0.02em; }
.block-container { padding-top: 2rem; max-width: 1150px; }
[data-testid="stSidebar"] { background: #fff; border-right: 1px solid #DDE2EC; }
.hero { background: #fff; border: 1px solid #DDE2EC; border-radius: 20px; padding: 2rem 2.2rem;
        display: flex; align-items: center; justify-content: space-between; gap: 2rem; flex-wrap: wrap; }
.hero h1 { font-size: 2.4rem; line-height: 1.1; margin: 0 0 .6rem 0; max-width: 560px; }
.hero p { color: #55607A; font-size: 1.05rem; margin: 0; max-width: 520px; }
.ring-wrap { position: relative; width: 190px; height: 190px; }
.ring-wrap .num { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.ring-wrap .num b { font-family: 'Bricolage Grotesque'; font-size: 2.8rem; line-height: 1; }
.ring-wrap .num span { font-size: .85rem; color: #55607A; }
.chip { display: inline-block; padding: .28rem .7rem; margin: .18rem .25rem .18rem 0; border-radius: 999px;
        font-size: .88rem; font-weight: 500; border: 1px solid transparent; }
.chip.have { background: #E3F5EE; color: #0A6E51; border-color: #BFE6D8; }
.chip.gap { background: #FDEBD9; color: #A24F05; border-color: #F6CFA8; }
.stat { background: #fff; border: 1px solid #DDE2EC; border-radius: 14px; padding: 1rem 1.2rem; }
.stat b { font-family: 'Bricolage Grotesque'; font-size: 1.9rem; display: block; line-height: 1.1; }
.stat span { color: #55607A; font-size: .9rem; }
.step { background: #fff; border: 1px solid #DDE2EC; border-left: 5px solid var(--c); border-radius: 12px;
        padding: .9rem 1.1rem; margin-bottom: .7rem; }
.step .t { font-family: 'Bricolage Grotesque'; font-size: 1.1rem; font-weight: 700; }
.step .m { color: #55607A; font-size: .9rem; margin-top: .15rem; }
:focus-visible { outline: 3px solid #2563EB !important; outline-offset: 2px; }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar: inputs ----------
with st.sidebar:
    st.markdown("### Skill Gap Analyzer")
    role = st.selectbox("Target role", list(ROLES), help="The job role you want to be ready for.")
    st.caption(ROLES[role]["desc"])
    st.divider()
    st.markdown("**Your skills**")
    resume = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
    picked = st.multiselect("Pick skills you know", sorted(CATALOG))
    typed = st.text_area("Or type them", placeholder="e.g. python, sql, power bi, docker, communication",
                         height=90)

have, resume_found = set(picked), set()
if resume is not None:
    try:
        resume_found = extract_skills(read_resume(resume))
        have |= resume_found
    except Exception as exc:  # unreadable or corrupted file
        st.sidebar.error(f"Could not read this file ({exc}). Try a PDF, DOCX or TXT export.")
if typed.strip():
    have |= extract_skills(typed.replace(",", " , "))

# ---------- Empty state ----------
if not have:
    st.markdown("""<div class="hero"><div>
<h1>See exactly which skills stand between you and your next role.</h1>
<p>Upload your resume or list what you know in the sidebar. You'll get a match score, the missing skills ranked by market demand, and a learning roadmap.</p>
</div></div>""", unsafe_allow_html=True)
    st.stop()

res = analyze(role, have)
score, circ = res["score"], 339.29
dash = circ * score / 100

# ---------- Hero with coverage ring ----------
st.markdown(f"""<div class="hero"><div>
<h1>You match {score}% of what {role} roles ask for.</h1>
<p>{verdict(score)}</p></div>
<div class="ring-wrap"><svg viewBox="0 0 120 120" width="190" height="190" role="img" aria-label="{score} percent match">
<circle cx="60" cy="60" r="54" fill="none" stroke="#FDEBD9" stroke-width="12"/>
<circle cx="60" cy="60" r="54" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round"
 stroke-dasharray="{dash:.1f} {circ}" transform="rotate(-90 60 60)"/></svg>
<div class="num"><b>{score}%</b><span>covered</span></div></div></div>""", unsafe_allow_html=True)

st.write("")
c1, c2, c3 = st.columns(3)
c1.markdown(f'<div class="stat"><b style="color:{TEAL}">{len(res["matched"])}</b><span>required skills you have</span></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="stat"><b style="color:{ORANGE}">{len(res["missing"])}</b><span>skills still missing</span></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="stat"><b>~{res["weeks"]} weeks</b><span>to close the gap, studied one skill at a time</span></div>', unsafe_allow_html=True)
st.write("")

if resume_found:
    st.caption(f"Found {len(resume_found)} skills in your resume: " + ", ".join(sorted(resume_found)))

tab1, tab2, tab3, tab4 = st.tabs(["Gap breakdown", "Skill balance", "Learning roadmap", "Other roles"])

with tab1:
    a, b = st.columns(2)
    with a:
        st.subheader("Skills you have")
        st.markdown("".join(f'<span class="chip have">{s}</span>' for s in res["matched"]) or "None of the required skills yet.", unsafe_allow_html=True)
    with b:
        st.subheader("Skills to learn")
        st.markdown("".join(f'<span class="chip gap">{s}</span>' for s in res["missing"]) or "No gaps. You cover everything.", unsafe_allow_html=True)
    extra = sorted(have - set(res["reqs"]))
    if extra:
        st.subheader("Other skills you listed")
        st.caption("Not required for this role, but they still count on a resume.")
        st.write(", ".join(extra))

with tab2:
    cats = res["by_category"]
    labels, vals = list(cats), list(cats.values())
    fig = go.Figure(go.Scatterpolar(r=vals + vals[:1], theta=labels + labels[:1], fill="toself",
                                    line=dict(color=TEAL, width=3), fillcolor="rgba(15,157,116,.25)"))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100], ticksuffix="%", gridcolor="#DDE2EC"),
                                 bgcolor="#fff"), showlegend=False, height=430,
                      margin=dict(l=60, r=60, t=30, b=30), paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Instrument Sans", color=INK))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Each axis shows how much of the role's demand in that area you already cover.")

with tab3:
    if not res["roadmap"]:
        st.success("Nothing left to learn for this role. Build a portfolio project and start applying.")
    else:
        st.caption("Ordered by market demand first, then by how quickly you can learn each skill.")
        colors = {"Critical": "#D93636", "Important": ORANGE, "Nice to have": "#7A869F"}
        for r in res["roadmap"]:
            st.markdown(f"""<div class="step" style="--c:{colors[r['priority']]}">
<div class="t">{r['skill']} <span style="font-weight:500;font-size:.85rem;color:{colors[r['priority']]}">{r['priority']}</span></div>
<div class="m">About {r['weeks']} weeks · {r['resource']}</div></div>""", unsafe_allow_html=True)

with tab4:
    ranking = rank_roles(have)
    fig = go.Figure(go.Bar(x=[s for _, s in ranking][::-1], y=[r for r, _ in ranking][::-1], orientation="h",
                           marker_color=[TEAL if r == role else "#B9C2D6" for r, _ in ranking][::-1],
                           text=[f"{s}%" for _, s in ranking][::-1], textposition="outside"))
    fig.update_layout(height=420, xaxis=dict(range=[0, 110], title="Match %"), plot_bgcolor="#fff",
                      paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=30, t=10, b=10),
                      font=dict(family="Instrument Sans", color=INK))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Your best fit right now: **{ranking[0][0]}** ({ranking[0][1]}%).")
