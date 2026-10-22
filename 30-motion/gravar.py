"""Grava um HTML animado (GSAP) em MP4, quadro a quadro, com relógio falso.

O claude.ai entrega o motion em HTML; o MP4 é um passo à parte (README).
O navegador não anda sozinho: Date.now, performance.now e requestAnimationFrame
são trocados antes da página carregar, e cada quadro avança 1/fps de segundo
exato. Assim o vídeo não depende da velocidade da máquina nem do pulo pela URL.
A página precisa expor a timeline do GSAP em window.tl (o index.html faz isso).

Uso: python gravar.py index.html teste.mp4 --seg 30
Pede: pip install playwright (usa o Google Chrome instalado; nada de baixar
navegador) e o ffmpeg no PATH ou em --ffmpeg.
"""
import argparse
import functools
import http.server
import pathlib
import shutil
import subprocess
import threading

from playwright.sync_api import sync_playwright

RELOGIO = """
(() => {
  let vt = 0;
  const base = Date.now();
  performance.now = () => vt;
  Date.now = () => base + vt;
  let fila = [];
  window.requestAnimationFrame = cb => { fila.push(cb); return fila.length; };
  window.cancelAnimationFrame = () => {};
  // sorteio com semente fixa (mulberry32): o stagger from:'random' da cena 7
  // mudava a ordem a cada gravação (README, Limites); o HTML da IA fica igual
  let semente = 30;
  Math.random = () => {
    semente = (semente + 0x6D2B79F5) | 0;
    let x = Math.imul(semente ^ (semente >>> 15), 1 | semente);
    x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
  window.__avancar = ms => {
    vt += ms;
    const c = fila; fila = [];
    c.forEach(f => f(vt));
    return vt;
  };
})();
"""


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def servir(pasta):
    h = functools.partial(Quieto, directory=str(pasta))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("mp4")
    ap.add_argument("--seg", type=float, default=30)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--largura", type=int, default=1920)
    ap.add_argument("--altura", type=int, default=1080)
    ap.add_argument("--ffmpeg", default=shutil.which("ffmpeg") or "ffmpeg")
    a = ap.parse_args()

    html = pathlib.Path(a.html).resolve()
    mp4 = pathlib.Path(a.mp4).resolve()
    quadros = mp4.with_suffix("")
    quadros = quadros.parent / (quadros.name + "-quadros")
    quadros.mkdir(parents=True, exist_ok=True)
    for p in quadros.glob("*.png"):
        p.unlink()

    srv = servir(html.parent)
    url = f"http://127.0.0.1:{srv.server_address[1]}/{html.name}"
    passo = 1000 / a.fps
    n = round(a.seg * a.fps)
    try:
        with sync_playwright() as pw:
            nav = pw.chromium.launch(channel="chrome", headless=True)
            try:
                pg = nav.new_page(viewport={"width": a.largura, "height": a.altura},
                                  device_scale_factor=1)
                pg.add_init_script(RELOGIO)
                pg.goto(url, wait_until="networkidle")
                pg.wait_for_function("window.tl !== undefined", timeout=10000)
                for i in range(n):
                    # o quadro i mostra o instante i/fps; o 1º avanço é zero
                    pg.evaluate("ms => window.__avancar(ms)", 0 if i == 0 else passo)
                    pg.screenshot(path=str(quadros / f"{i:04d}.png"))
                    if i % (a.fps * 5) == 0:
                        t = pg.evaluate("window.tl.time()")
                        print(f"quadro {i:4d}  esperado {i / a.fps:6.2f} s  tl {t:6.2f} s", flush=True)
            finally:
                nav.close()
    finally:
        srv.shutdown()

    subprocess.run([a.ffmpeg, "-y", "-loglevel", "error", "-framerate", str(a.fps),
                    "-i", str(quadros / "%04d.png"), "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", str(mp4)], check=True)
    print(f"{n} quadros -> {mp4}")


if __name__ == "__main__":
    main()
