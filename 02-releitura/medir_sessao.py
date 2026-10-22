"""Onde os tokens de uma sessão do Claude Code foram gastos.

Uso: python -I medir_sessao.py <transcrição .jsonl de uma sessão do Claude Code>

Lê a transcrição (um JSON por linha) e soma o `usage` de cada resposta:
releitura do cache (`cache_read_input_tokens`), gravação do cache
(`cache_creation_input_tokens`), entrada nova (`input_tokens`) e saída
(`output_tokens`). Uma resposta grava um bloco por linha e repete o `usage`
em todas: conta uma vez por `message.id`. Também mostra o contexto por
resposta, os reinícios de cache (mais de 100 mil tokens gravados de uma vez)
e quanto texto cada ferramenta devolveu.

Origem: cópia, feita em 21/10/2026, do medidor de uso interno que fez o
post 2 da @peterwk.dev. A conta é a mesma; saiu
o `--provar`, que virou `tests/test_02_releitura.py`, com transcrição
sintética. Medida de 29/09/2026 (contagem corrigida em 01/10): 96% de
releitura e 0,2% de saída; a de 18/10/2026 está em `medicao-1810.txt`.

Lê só a transcrição que você indicar e não grava nada: a saída vai para a
tela. A transcrição é sua e tem dado da conta: não a publique.
"""
import collections
import contextlib
import io
import json
import sys
from pathlib import Path


def medir(caminho: Path) -> None:
    uso = collections.Counter()
    contextos, reescritas = [], []
    por_ferramenta = collections.Counter()
    vezes = collections.Counter()
    nome_por_id = {}
    vistos = set()  # uma resposta grava um bloco por linha e repete o usage em todas
    for linha in caminho.open(encoding="utf-8"):
        try:
            e = json.loads(linha)
        except ValueError:
            continue
        m = e.get("message") or {}
        u = m.get("usage")
        mid = m.get("id")
        if e.get("type") == "assistant" and u and (mid is None or mid not in vistos):
            vistos.add(mid)
            for k in ("input_tokens", "cache_creation_input_tokens",
                      "cache_read_input_tokens", "output_tokens"):
                uso[k] += u.get(k) or 0
            gravado = u.get("cache_creation_input_tokens") or 0
            contextos.append(gravado + (u.get("cache_read_input_tokens") or 0)
                             + (u.get("input_tokens") or 0))
            if gravado > 100_000:
                reescritas.append(gravado)
        conteudo = m.get("content")
        if not isinstance(conteudo, list):
            continue
        for b in conteudo:
            if b.get("type") == "tool_use":
                nome_por_id[b["id"]] = b["name"]
            elif b.get("type") == "tool_result":
                c = b.get("content")
                texto = c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)
                nome = nome_por_id.get(b.get("tool_use_id"), "?")
                por_ferramenta[nome] += len(texto)
                vezes[nome] += 1

    total = sum(uso.values()) or 1
    print(f"transcript: {caminho.name}  ({caminho.stat().st_size / 1e6:.1f} MB)")
    print(f"respostas: {len(contextos)}")
    for k, v in uso.most_common():
        print(f"  {k:30} {v:>14,}  {100 * v / total:5.1f}%")
    if contextos:
        s = sorted(contextos)
        print(f"contexto por resposta: mediana {s[len(s) // 2]:,} · "
              f"p90 {s[int(len(s) * 0.9)]:,} · máx {s[-1]:,}")
    print(f"reinícios de cache (> 100 mil gravados): {len(reescritas)}, "
          f"somando {sum(reescritas):,}")
    print("resultado de ferramenta (caracteres):")
    for nome, ch in por_ferramenta.most_common(8):
        print(f"  {nome[:45]:45} {vezes[nome]:4}x {ch:>10,}")


def saida(caminho: Path) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        medir(caminho)
    return buf.getvalue()


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    medir(Path(argv[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
