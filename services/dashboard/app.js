async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return res.json();
}

function pct(v) {
  if (v === null || v === undefined) return "—";
  return `${Math.round(Number(v) * 100)}%`;
}

function renderOverview(data) {
  document.getElementById("kpi-statements").textContent = data.statements ?? 0;
  document.getElementById("kpi-learners").textContent = data.learners ?? 0;
  document.getElementById("kpi-risk").textContent = data.at_risk ?? 0;
  document.getElementById("kpi-engagement").textContent = pct(data.avg_engagement);
}

function renderLearners(data) {
  const body = document.getElementById("learners-body");
  body.innerHTML = "";
  for (const l of data.learners || []) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${l.actor_name || l.actor_mbox}</td>
      <td>${pct(l.engagement_score)}</td>
      <td>${pct(l.risk_score)}</td>
      <td><span class="pill ${l.risk_level || "low"}">${l.risk_level || "n/a"}</span></td>
      <td>${pct(l.quiz_avg_score)}</td>
      <td>${l.total_statements ?? 0}</td>
    `;
    body.appendChild(tr);
  }
}

function renderRemediations(data) {
  const list = document.getElementById("remediations");
  list.innerHTML = "";
  for (const r of data.remediations || []) {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${r.actor_name} · ${r.risk_level} (${pct(r.risk_score)})</strong><span>${r.remediation}</span>`;
    list.appendChild(li);
  }
  if (!(data.remediations || []).length) {
    list.innerHTML = "<li><strong>Aucune remédiation urgente</strong><span>Les scores se stabilisent.</span></li>";
  }
}

function renderCourses(data) {
  const body = document.getElementById("courses-body");
  body.innerHTML = "";
  for (const c of data.courses || []) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${c.course_id}</td>
      <td>${c.learners}</td>
      <td>${c.statements}</td>
      <td>${pct(c.avg_quiz_score)}</td>
    `;
    body.appendChild(tr);
  }
}

async function refresh() {
  try {
    const [overview, learners, remediations, courses] = await Promise.all([
      fetchJson("/api/overview"),
      fetchJson("/api/learners?limit=30"),
      fetchJson("/api/remediations?limit=12"),
      fetchJson("/api/courses"),
    ]);
    renderOverview(overview);
    renderLearners(learners);
    renderRemediations(remediations);
    renderCourses(courses);
  } catch (err) {
    console.error(err);
  }
}

refresh();
setInterval(refresh, 15000);
