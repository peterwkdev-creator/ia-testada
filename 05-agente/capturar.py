"""Capturas do Reel do post 6: páginas oficiais com a frase citada em destaque.

Chrome sem tela, com um perfil próprio e vazio (`%TEMP%\\carrossel-chrome-headless`
no Windows; a pasta temporária do sistema nos outros): não usa o seu perfil do
Chrome, os seus logins nem os seus cookies, e só abre as páginas públicas da
lista `PAGINAS`. Controle pelo protocolo de depuração (CDP), com o
`websockets`. Para cada página: abre, tira banner de cookies, acha a frase
(`window.find`), marca a frase com um retângulo por cima, centraliza e
recorta uma faixa de 1080 px de largura. Grava `capturas/<nome>.png` e
`capturas/capturas.tsv` (nome, URL, frase, resultado, data UTC).

Origem: cópia de 21/10/2026 do script que fez as capturas do post (a
versão que rodou em 20/10/2026). Mudou só o que não altera a captura: o
`websockets` é importado na hora de capturar, o caminho do Chrome aceita a
variável `CHROME`, e o recorte e o tsv saíram em funções puras, testadas
em `tests/test_05_capturar.py` (o CI não abre Chrome nem rede).

Uso: python capturar.py   (precisa de `pip install websockets` e do Chrome)
"""

import asyncio
import base64
import datetime
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "capturas"
CHROME = os.environ.get(
    "CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
PORTA = 9333
LARG, ALT_JANELA, ALT_RECORTE = 1080, 1600, 820

PAGINAS = [
    ("projeto",
     "https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing",
     "Everyone in your organization can view and use the project"),
    ("artefato",
     "https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them",
     "usage counts against each person's own plan limits"),
]

CABECALHO = "nome\turl\tfrase\tresultado\tdata\n"

JS_MARCAR = r"""
(frase) => {
  for (const sel of ['#onetrust-banner-sdk', '#onetrust-consent-sdk',
                     '[id*="cookie" i]', '[class*="cookie" i]',
                     '[aria-label*="cookie" i]']) {
    document.querySelectorAll(sel).forEach(e => e.remove());
  }
  const variantes = [frase, frase.replace(/'/g, '\u2019')];
  let achou = null;
  for (const v of variantes) {
    getSelection().removeAllRanges();
    window.scrollTo(0, 0);
    if (window.find(v, false, false, true, false, false, false)) { achou = v; break; }
  }
  if (!achou) return {ok: false};
  const r = getSelection().getRangeAt(0);
  r.startContainer.parentElement.scrollIntoView({block: 'center'});
  const caixas = Array.from(r.getClientRects());
  getSelection().removeAllRanges();
  for (const c of caixas) {
    const d = document.createElement('div');
    Object.assign(d.style, {
      position: 'absolute', left: (c.left + scrollX - 4) + 'px',
      top: (c.top + scrollY - 3) + 'px', width: (c.width + 8) + 'px',
      height: (c.height + 6) + 'px', background: 'rgba(61, 220, 132, 0.30)',
      outline: '3px solid #2fb36b', borderRadius: '4px',
      pointerEvents: 'none', zIndex: 99999});
    document.body.appendChild(d);
  }
  const topo = Math.min(...caixas.map(c => c.top)) + scrollY;
  return {ok: true, variante: achou, topo: topo, h: document.documentElement.scrollHeight};
}
"""


def recorte_y(topo, altura_pagina):
    """Topo da faixa recortada: 300 px acima da frase, sem passar do fim nem do começo."""
    return max(0, min(topo - 300, altura_pagina - ALT_RECORTE))


def texto_tsv(linhas, agora):
    """O capturas.tsv: cabeçalho e uma linha por página, todas com a mesma data."""
    return CABECALHO + "".join("\t".join(linha) + f"\t{agora}\n" for linha in linhas)


def tudo_ok(linhas):
    return all(linha[3] == "ok" for linha in linhas)


class Cdp:
    def __init__(self, ws):
        self.ws, self.n = ws, 0

    async def __call__(self, metodo, **params):
        self.n += 1
        meu = self.n
        await self.ws.send(json.dumps({"id": meu, "method": metodo, "params": params}))
        while True:
            msg = json.loads(await self.ws.recv())
            if msg.get("id") == meu:
                if "error" in msg:
                    raise RuntimeError(f"{metodo}: {msg['error']}")
                return msg.get("result", {})

    async def esperar(self, evento, limite=30):
        fim = time.time() + limite
        while time.time() < fim:
            try:
                msg = json.loads(await asyncio.wait_for(self.ws.recv(), 1))
            except asyncio.TimeoutError:
                continue
            if msg.get("method") == evento:
                return msg
        raise TimeoutError(evento)


async def capturar(url_ws):
    import websockets  # só aqui: o resto do script (e os testes) roda sem ele

    linhas = []
    async with websockets.connect(url_ws, max_size=None) as ws:
        cdp = Cdp(ws)
        await cdp("Page.enable")
        await cdp("Emulation.setDeviceMetricsOverride", width=LARG,
                  height=ALT_JANELA, deviceScaleFactor=1, mobile=False)
        for nome, url, frase in PAGINAS:
            await cdp("Page.navigate", url=url)
            await cdp.esperar("Page.loadEventFired")
            await asyncio.sleep(3)
            res = await cdp("Runtime.evaluate", returnByValue=True,
                            expression=f"({JS_MARCAR})({json.dumps(frase)})")
            val = res["result"].get("value") or {}
            if not val.get("ok"):
                titulo = await cdp("Runtime.evaluate", returnByValue=True,
                                   expression="document.title")
                print(f"{nome}: frase NÃO achada (título: "
                      f"{titulo['result'].get('value')!r})")
                linhas.append((nome, url, frase, "não achada"))
                continue
            y = recorte_y(val["topo"], val["h"])
            img = await cdp("Page.captureScreenshot", format="png",
                            captureBeyondViewport=True,
                            clip={"x": 0, "y": y, "width": LARG,
                                  "height": ALT_RECORTE, "scale": 1})
            (SAIDA / f"{nome}.png").write_bytes(base64.b64decode(img["data"]))
            print(f"{nome}: ok (y={y:.0f}, variante {val['variante']!r})")
            linhas.append((nome, url, frase, "ok"))
    return linhas


def main():
    SAIDA.mkdir(exist_ok=True)
    perfil = pathlib.Path(tempfile.gettempdir()) / "carrossel-chrome-headless"
    proc = subprocess.Popen([
        CHROME, "--headless=new", f"--remote-debugging-port={PORTA}",
        f"--user-data-dir={perfil}", f"--window-size={LARG},{ALT_JANELA}",
        "--hide-scrollbars", "--lang=en-US", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        alvos = None
        for _ in range(40):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORTA}/json") as r:
                    alvos = json.load(r)
                break
            except OSError:
                time.sleep(0.25)
        if not alvos:
            sys.exit("erro: Chrome sem tela não respondeu")
        pagina = next(a for a in alvos if a.get("type") == "page")
        linhas = asyncio.run(capturar(pagina["webSocketDebuggerUrl"]))
    finally:
        proc.terminate()
        proc.wait(10)
    agora = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(SAIDA / "capturas.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write(texto_tsv(linhas, agora))
    if not tudo_ok(linhas):
        sys.exit(1)


if __name__ == "__main__":
    main()
