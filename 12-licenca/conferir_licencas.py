"""Confere a licença do CÓDIGO e a dos PESOS de seis modelos abertos de IA.

Uso: python -I conferir_licencas.py

Para cada modelo, lê dois metadados públicos, sem token e só com a biblioteca
padrão:

1. código: API do GitHub, GET /repos/{dono}/{repo}, campo license.spdx_id
   (null quando o repositório não declara licença);
2. pesos: API do Hugging Face, GET /api/models/{id}, campos cardData.license
   e cardData.license_name (ou, na falta deles, a tag "license:...").

Grava em medidas.tsv (nesta pasta) uma linha por modelo, com a data UTC da
coleta. É a licença declarada nos metadados, não um parecer jurídico. Se a
API limitar ou falhar, o script para com o erro, sem inventar valor.
"""
import csv
import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
URL_GITHUB = "https://api.github.com/repos/{repo}"
URL_HF = "https://huggingface.co/api/models/{id}"
CABECALHO = ("modelo", "repo_github", "licenca_codigo", "id_hf", "licenca_pesos",
             "nome_licenca_pesos", "coletado_em")
MODELOS = (
    ("F5-TTS", "SWivid/F5-TTS", "SWivid/F5-TTS"),
    ("XTTS-v2", "idiap/coqui-ai-TTS", "coqui/XTTS-v2"),
    ("LTX-2", "Lightricks/LTX-2", "Lightricks/LTX-2"),
    ("Kokoro (kokoro-onnx)", "thewh1teagle/kokoro-onnx", "hexgrad/Kokoro-82M"),
    ("Piper (vozes)", "OHF-Voice/piper1-gpl", "rhasspy/piper-voices"),
    ("Whisper (small)", "SYSTRAN/faster-whisper", "Systran/faster-whisper-small"),
)
VAZIO = "(nenhuma)"


def licenca_codigo(dados):
    """spdx_id do JSON do repositório no GitHub, ou VAZIO se não houver licença."""
    licenca = dados.get("license") or {}
    return licenca.get("spdx_id") or VAZIO


def licenca_pesos(dados):
    """(licença, nome da licença) do JSON do modelo no Hugging Face."""
    card = dados.get("cardData") or {}
    licenca = card.get("license")
    if isinstance(licenca, list):
        licenca = ",".join(licenca)
    if not licenca:
        tags = [t[len("license:"):] for t in dados.get("tags") or [] if t.startswith("license:")]
        licenca = ",".join(tags)
    return licenca or VAZIO, card.get("license_name") or ""


def ler_json(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "ia-testada-conferir-licencas",
                                                  "Accept": "application/json"})
    try:
        with urllib.request.urlopen(pedido, timeout=30) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        raise SystemExit(f"{url} respondeu {erro.code}: {erro.reason}")
    except urllib.error.URLError as erro:
        raise SystemExit(f"{url} sem resposta: {erro.reason}")


def medir(quando):
    linhas = []
    for modelo, repo, id_hf in MODELOS:
        codigo = licenca_codigo(ler_json(URL_GITHUB.format(repo=repo)))
        pesos, nome = licenca_pesos(ler_json(URL_HF.format(id=id_hf)))
        linhas.append((modelo, repo, codigo, id_hf, pesos, nome, quando))
    return linhas


def gravar(linhas, destino):
    with open(destino, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter="\t", lineterminator="\n")
        escritor.writerow(CABECALHO)
        escritor.writerows(linhas)


def main(argv=None, destino=AQUI / "medidas.tsv", quando=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        raise SystemExit(__doc__)
    if quando is None:
        quando = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    linhas = medir(quando)
    gravar(linhas, destino)
    print(pathlib.Path(destino).read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
