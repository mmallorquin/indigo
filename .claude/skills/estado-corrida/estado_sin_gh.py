#!/usr/bin/env python3
"""Estado del repo sin gh autenticado: lee las páginas públicas de GitHub (solo lectura).

Uso: python3 .claude/skills/estado-corrida/estado_sin_gh.py [owner/repo] [issue_avisos]
"""
import html
import json
import re
import subprocess
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else "mmallorquin/indigo"
AVISOS = sys.argv[2] if len(sys.argv) > 2 else "3"


def bajar(ruta):
    r = subprocess.run(["curl", "-sL", "--max-time", "30", f"https://github.com/{REPO}/{ruta}"],
                       capture_output=True, text=True)
    return r.stdout


def datos_embebidos(pagina):
    for m in re.finditer(r'<script type="application/json" data-target="react-app.embeddedData">(.*?)</script>',
                         pagina, re.S):
        try:
            yield json.loads(m.group(1))
        except json.JSONDecodeError:
            pass


def recorrer(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from recorrer(v)
    elif isinstance(o, list):
        for v in o:
            yield from recorrer(v)


def issues_abiertos():
    p = bajar("issues?q=is%3Aissue+is%3Aopen")
    vistos = {}
    for n, t in re.findall(r'"number":(\d+),"title":"((?:[^"\\]|\\.)*)"', p):
        vistos[int(n)] = json.loads(f'"{t}"')
    print("## Issues abiertos")
    for n in sorted(vistos):
        print(f"#{n} {vistos[n]}")


def prs_abiertos():
    p = bajar("pulls?q=is%3Apr+is%3Aopen")
    print("\n## PR abiertos")
    vistos = {}
    for n, t in re.findall(r'/pull/(\d+)","repoNameWithOwner":"[^"]*","state":"REPO_PULL_REQUEST_STATE_OPEN","title":"((?:[^"\\]|\\.)*)"', p):
        vistos[int(n)] = json.loads(f'"{t}"')
    for n in sorted(vistos):
        print(f"#{n} {vistos[n]}  (checks: abrir https://github.com/{REPO}/pull/{n}/checks)")


def corridas():
    p = bajar("actions")
    print("\n## Últimas corridas de Actions")
    for i, m in enumerate(re.finditer(r'aria-label="((?:completed successfully|failed|cancelled|skipped|in progress|queued)[^"]*)"', p)):
        if i >= 15:
            break
        print(html.unescape(m.group(1))[:160])


def comentarios_avisos():
    p = bajar(f"issues/{AVISOS}")
    vistos, lista = set(), []
    for d in datos_embebidos(p):
        for o in recorrer(d):
            cuerpo = o.get("body")
            if isinstance(cuerpo, str) and len(cuerpo) > 20 and cuerpo not in vistos:
                vistos.add(cuerpo)
                autor = (o.get("author") or {}).get("login")
                lista.append((o.get("createdAt") or "", autor, cuerpo))
    print(f"\n## Últimos comentarios del issue #{AVISOS} (la página pública puede no traerlos todos)")
    for fecha, autor, cuerpo in lista[-10:]:
        print(f"--- {autor} {fecha}\n{cuerpo[:1200]}")


if __name__ == "__main__":
    issues_abiertos()
    prs_abiertos()
    corridas()
    comentarios_avisos()
