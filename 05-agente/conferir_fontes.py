"""Confere se as frases que o post cita ainda estão nas páginas oficiais.

Uso: python -I conferir_fontes.py

Baixa cada página de FONTES, tira o HTML e confere, frase a frase, se o
trecho citado ainda está lá. A saída vai para conferencia.tsv (nesta pasta),
com a data e a hora da leitura (UTC). Sai com código 1 se alguma frase
sumiu ou alguma página não abriu: aí o post precisa ser revisto.

Página de documentação muda sem aviso. O que vale é a data da leitura.
"""
import datetime
import html
import http.client
import pathlib
import re
import sys
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent

# (nome curto, URL, frases citadas no post, como estão na página em inglês)
FONTES = [
    ("projeto-compartilhar",
     "https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing",
     ["Project visibility and sharing features are available to users on Team or Enterprise plans",
      "Everyone in your organization can view and use the project"]),
    ("artefatos",
     "https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them",
     ["Artifacts start private to you",
      "No API keys are required",
      "usage counts against each person's own plan limits rather than yours"]),
    ("agent-sdk",
     "https://code.claude.com/docs/en/agent-sdk/overview",
     ["Unless previously approved, Anthropic does not allow third party "
      "developers to offer claude.ai login or rate limits for their products"]),
    ("managed-agents",
     "https://platform.claude.com/docs/en/managed-agents/overview",
     ["Claude Managed Agents is in beta",
      "harness and infrastructure for running Claude as an autonomous agent",
      "Recurring agent runs on a cron schedule through scheduled deployments",
      "A Claude API key from the Claude Console"]),
    ("precos",
     "https://platform.claude.com/docs/en/about-claude/pricing",
     ["Claude Managed Agents is billed on two dimensions: tokens and session runtime",
      "All tokens consumed by a Claude Managed Agents session are billed at the rates shown in Model pricing"]),
    ("projects-claude-code",
     "https://code.claude.com/docs/en/claude-projects",
     ["You can't share a project or its threads with another user",
      "public beta on Pro and Max plans",
      "Projects in claude.ai chat and Cowork"]),
]

ASPAS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"',
                       " ": " "})


def texto(pagina):
    """O texto visível de uma página HTML, numa linha, com aspas retas."""
    pagina = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", pagina)
    pagina = re.sub(r"(?s)<[^>]+>", " ", pagina)
    return normal(html.unescape(pagina))


def normal(t):
    """Aspas tipográficas viram retas e todo espaço vira um só."""
    return re.sub(r"\s+", " ", t.translate(ASPAS)).strip()


def conferir(pagina, frases):
    """Para cada frase, se ela está no texto da página (sem diferenciar caixa)."""
    corpo = texto(pagina).casefold()
    return [(f, normal(f).casefold() in corpo) for f in frases]


def baixar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "ia-testada/conferir_fontes"})
    with urllib.request.urlopen(pedido, timeout=30) as r:
        return r.status, r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


def tabela(linhas, quando):
    saida = [f"# lido em {quando} (UTC)", "fonte\turl\thttp\tfrase\tpresente"]
    saida += ["\t".join(map(str, l)) for l in linhas]
    return "\n".join(saida) + "\n"


def main():
    quando = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    linhas, falhou = [], False
    for nome, url, frases in FONTES:
        try:
            status, pagina = baixar(url)
            achadas = conferir(pagina, frases)
        except (OSError, http.client.HTTPException) as erro:
            status, achadas = f"erro: {erro}", [(f, False) for f in frases]
        for frase, ok in achadas:
            linhas.append((nome, url, status, frase, "sim" if ok else "não"))
            falhou |= not ok
    (AQUI / "conferencia.tsv").write_bytes(tabela(linhas, quando).encode("utf-8"))
    for l in linhas:
        print(f"{l[4]:>3}  {l[0]}: {l[3][:70]}")
    print(f"lido em {quando} UTC; {sum(l[4] == 'sim' for l in linhas)} de {len(linhas)} frases")
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
