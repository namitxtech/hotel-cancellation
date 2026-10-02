export function Ring({ score }: { score: number }) {
  const c = 339.29;
  return (
    <div className="ring">
      <svg viewBox="0 0 120 120" role="img" aria-label={`${score} percent match`}>
        <circle cx="60" cy="60" r="54" className="ring-bg" />
        <circle cx="60" cy="60" r="54" className="ring-fg" strokeDasharray={`${(c * score) / 100} ${c}`}
          transform="rotate(-90 60 60)" />
      </svg>
      <div className="ring-num"><b>{score}%</b><span>covered</span></div>
    </div>
  );
}

export function Radar({ data }: { data: Record<string, number> }) {
  const keys = Object.keys(data), n = keys.length, C = 170, R = 105;
  const pt = (i: number, v: number) => {
    const a = (Math.PI * 2 * i) / n - Math.PI / 2;
    return [C + Math.cos(a) * R * v / 100, C + Math.sin(a) * R * v / 100];
  };
  const poly = (f: (i: number) => number) => keys.map((_, i) => pt(i, f(i)).join(",")).join(" ");
  return (
    <svg viewBox="-50 0 440 340" className="radar" role="img"
      aria-label={"Skill coverage by category: " + keys.map((k) => `${k} ${data[k]}%`).join(", ")}>
      {[25, 50, 75, 100].map((g) => <polygon key={g} points={poly(() => g)} className="grid" />)}
      {keys.map((k, i) => {
        const [x, y] = pt(i, 100), [lx, ly] = pt(i, 124);
        return (
          <g key={k}>
            <line x1={C} y1={C} x2={x} y2={y} className="grid" />
            <text x={lx} y={ly} dy="0.35em" className="axis"
              textAnchor={lx < C - 6 ? "end" : lx > C + 6 ? "start" : "middle"}>{k} · {data[k]}%</text>
          </g>
        );
      })}
      <polygon points={poly((i) => data[keys[i]])} className="area" />
      {keys.map((k, i) => { const [x, y] = pt(i, data[k]); return <circle key={k} cx={x} cy={y} r="4" className="dot" />; })}
    </svg>
  );
}
