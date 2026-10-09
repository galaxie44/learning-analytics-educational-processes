#!/usr/bin/env python3
"""Fill Labs Report DOCX with real captures and Hub URLs."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(r"c:\Users\edoua\Desktop\Master SIGLIS\Cloud computing\Projet")
CAP = ROOT / "docs" / "captures" / "labs"
OUTS = [
    Path(r"c:\Users\edoua\Downloads\Report of Cloud Computing Labs - COMPLETE.docx"),
    Path(r"c:\Users\edoua\Downloads\Report of Cloud Computing Labs.docx"),
    ROOT / "docs" / "livrables" / "Report-Cloud-Computing-Labs.docx",
]


def set_run(run, size=11, bold=False, italic=False, color=None):
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color


def h(doc, text, level=1):
    x = doc.add_heading(text, level=level)
    for r in x.runs:
        r.font.color.rgb = RGBColor(0x0F, 0x2C, 0x4C)


def p(doc, text, bold=False, italic=False):
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_run(run, bold=bold, italic=italic)
    return para


def bullets(doc, items):
    for it in items:
        para = doc.add_paragraph(it, style="List Bullet")
        for r in para.runs:
            set_run(r)


def img(doc, path: Path, width=6.2, caption=None):
    if not path.exists():
        p(doc, f"[missing image: {path.name}]", italic=True)
        return
    doc.add_picture(str(path), width=Inches(width))
    if caption:
        cap = doc.add_paragraph()
        r = cap.add_run(caption)
        set_run(r, size=9, italic=True, color=RGBColor(0x55, 0x55, 0x55))


def main():
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)

    t = doc.add_heading("Cloud Computing Docker course", 0)
    for r in t.runs:
        r.font.color.rgb = RGBColor(0x0F, 0x2C, 0x4C)
    s = doc.add_paragraph()
    r = s.add_run("Learning Outcomes Report — Labs 5 to 8")
    set_run(r, size=14, bold=True)
    s.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p(doc, "Student Name: Edouard CLEMENCEAU")
    p(doc, "Student email: eclemence001@univ-pau.fr")
    p(doc, "Course: SIGLIS M1 — Cloud Computing I (Docker & containers)")
    p(doc, "GitHub project: https://github.com/galaxie44/learning-analytics-educational-processes")

    h(doc, "1. Personal hub.docker.com registry")
    p(doc, "My Docker Hub account:")
    p(doc, "https://hub.docker.com/u/edouardclemenceau", bold=True)
    p(doc, "Images I pushed for the labs / project:")
    bullets(
        doc,
        [
            "https://hub.docker.com/r/edouardclemenceau/lrs-api",
            "https://hub.docker.com/r/edouardclemenceau/analytics-api",
            "https://hub.docker.com/r/edouardclemenceau/la-dashboard",
        ],
    )

    h(doc, "2. LAB 5 — Optimising a Dockerfile")
    p(
        doc,
        "A Dockerfile is Infrastructure-as-Code for container images: it declares the base image, "
        "dependencies, copied source files, exposed ports and the startup command. Docker builds a "
        "reproducible image from that recipe.",
    )
    p(doc, "How I solved Lab 5", bold=True)
    p(
        doc,
        "I optimised Dockerfiles for the Learning Analytics microservices (example: services/lrs-api): "
        "slim Python base image, dependency layer cached before source copy, --no-cache-dir pip install, "
        "and a HEALTHCHECK. This reduces image size and rebuild time.",
    )
    p(doc, "Access / ports", bold=True)
    bullets(
        doc,
        [
            "Local LRS API: http://localhost:8200/health",
            "Local Analytics API: http://localhost:8210/health",
            "EVA (VPN): http://10.3.16.179:8200 and :8210",
        ],
    )
    p(doc, "Image URL", bold=True)
    p(doc, "https://hub.docker.com/r/edouardclemenceau/lrs-api :latest")
    p(doc, "Screenshots", bold=True)
    img(doc, CAP / "lab5-dockerfile.png", caption="Figure Lab5 — Dockerfile (lrs-api)")
    img(doc, CAP / "docker-images.png", caption="Figure Lab5 — Local Docker images after build")

    h(doc, "3. LAB 6 — Using the Compose specification")
    p(
        doc,
        "Docker Compose describes a multi-container application in YAML (services, networks, volumes, env). "
        "One command starts the whole stack: docker compose up --build -d.",
    )
    p(doc, "How I solved Lab 6", bold=True)
    p(
        doc,
        "I defined postgres + application services with a shared network and a named volume pgdata for "
        "external persistency. After docker compose down && up, analytics data remained available via /api/overview.",
    )
    p(doc, "Access / ports", bold=True)
    bullets(
        doc,
        [
            "http://localhost:8210/api/overview",
            "http://localhost:8300 (dashboard)",
            "Postgres localhost:5432",
            "EVA: http://10.3.16.179:8210 and :8300",
        ],
    )
    p(doc, "Image / repo", bold=True)
    p(doc, "postgres:16-alpine + https://hub.docker.com/r/edouardclemenceau/analytics-api")
    p(doc, "Screenshots", bold=True)
    img(doc, CAP / "docker-compose-ps.png", caption="Figure Lab6 — docker compose ps")
    img(doc, CAP / "docker-volumes.png", caption="Figure Lab6 — named volumes (persistency)")
    img(doc, CAP / "lab8-api-overview.png", caption="Figure Lab6/8 — API overview JSON")

    h(doc, "4. LAB 7 — Portal container to administer Docker (Portainer)")
    p(
        doc,
        "Lab 7 deploys Portainer, a web portal that administers Docker (containers, images, volumes, stacks) "
        "by mounting the Docker socket.",
    )
    p(doc, "How I solved Lab 7", bold=True)
    p(
        doc,
        "I enabled the Compose profile ops: docker compose --profile ops up -d. "
        "Portainer CE 2.21.4 listens on port 9000. I created the admin user and inspected the local environment "
        "(stacks / containers / volumes / images).",
    )
    p(doc, "Access / ports", bold=True)
    bullets(
        doc,
        [
            "http://localhost:9000",
            "EVA: http://10.3.16.179:9000 (VPN)",
            "Image: portainer/portainer-ce:2.21.4",
        ],
    )
    p(doc, "Screenshots", bold=True)
    img(doc, CAP / "lab7-portainer-setup.png", caption="Figure Lab7 — Portainer initial admin setup")
    img(doc, CAP / "lab7-portainer-home.png", caption="Figure Lab7 — Portainer Home (local environment)")
    if (CAP / "lab7-portainer-containers.png").exists():
        img(doc, CAP / "lab7-portainer-containers.png", caption="Figure Lab7 — Containers view")

    h(doc, "4. LAB 8 — Compose multi-container Learning Analytics stack")
    p(
        doc,
        "For Lab 8 I ran the full Compose SaaS stack: generator → LRS → Postgres → analytics worker → API → dashboard. "
        "Restart policy is on-failure:3 (not unlimited) to respect the EVA/Proxmox guidance.",
    )
    p(doc, "Access / ports", bold=True)
    bullets(
        doc,
        [
            "Dashboard: http://localhost:8300",
            "API overview: http://localhost:8210/api/overview",
            "LRS health: http://localhost:8200/health",
            "EVA: http://10.3.16.179:8300 / :8210 / :8200",
        ],
    )
    p(doc, "Images pushed", bold=True)
    bullets(
        doc,
        [
            "https://hub.docker.com/r/edouardclemenceau/lrs-api",
            "https://hub.docker.com/r/edouardclemenceau/analytics-api",
            "https://hub.docker.com/r/edouardclemenceau/la-dashboard",
        ],
    )
    p(doc, "Screenshots", bold=True)
    img(doc, CAP / "lab8-dashboard.png", caption="Figure Lab8 — Learning Analytics dashboard")
    img(doc, CAP / "lab8-api-overview.png", caption="Figure Lab8 — /api/overview KPIs")
    img(doc, CAP / "docker-compose-ops.png", caption="Figure Lab8 — Compose stack including Portainer profile")

    h(doc, "Conclusion")
    p(
        doc,
        "Labs 5–8 covered Dockerfile optimisation, Compose + persistency, Portainer administration, and a full "
        "multi-service Compose application. The same stack is used for our course project on EVA.",
    )

    for out in OUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        doc.save(out)
        print("Saved", out)


if __name__ == "__main__":
    main()
