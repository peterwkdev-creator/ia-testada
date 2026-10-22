# 04-vozes: 6 vozes abertas leem a mesma frase

Medida do post "Claude Code em voz alta: 6 vozes abertas de IA leram a
mesma frase, e o Whisper contou os erros" da @peterwk.dev (post 4,
programado para 23/10/2026).

**Medido em 19/10/2026, com a versão r10 do nosso TTS**, Whisper small em
CPU, modelos abertos Kokoro-82M e Piper.

O código e a medida ficam no repositório do TTS, onde a legenda do post
aponta: **[tts-ptbr/exemplos](https://github.com/peterwkdev-creator/tts-ptbr/tree/main/exemplos)**
(o script das 6 vozes, `05_vozes.py`, e a medida desta rodada,
`vozes_medidas.tsv`). Esta pasta só explica e aponta, para não haver duas
cópias do mesmo código.

## O que mede

A mesma frase ("Medi no Claude Code: 96% dos tokens são releitura.", 13
palavras faladas) lida uma vez por 6 vozes abertas, transcrita pelo Whisper
e comparada palavra a palavra com o texto: quantas palavras cada voz errou.

## Pré-requisitos

Os do `tts-ptbr`, descritos no README de lá: Python 3.12, o
[ffmpeg](https://ffmpeg.org/download.html) no PATH e os modelos (o Kokoro e
as 3 vozes do Piper, pelo `baixar_modelos.py`; o Whisper small, ~480 MB,
baixa na 1ª medida). Roda em CPU, sem placa de vídeo.

## Passo a passo

Os três `requirements*.txt` do `tts-ptbr` não se misturam: cada etapa roda
no seu ambiente virtual (`python -m venv`). A instalação mínima e a 1ª
etapa, no ambiente do `requirements.txt`:

```bash
git clone https://github.com/peterwkdev-creator/tts-ptbr.git
cd tts-ptbr
python -m pip install -r requirements.txt && python baixar_modelos.py
python exemplos/05_vozes.py kokoro
```

As outras duas, cada uma no seu ambiente, na mesma pasta:

```bash
python -m pip install -r requirements-piper.txt
python exemplos/05_vozes.py piper
```

```bash
python -m pip install -r requirements-medir.txt
python exemplos/05_vozes.py medir
```

Grava em `saida/vozes/` (fora do git) um `<voz>.wav` por voz e o
`medidas.tsv`.

## Saída esperada

Uma tabela com uma linha por voz, como a do `vozes_medidas.tsv`: `voz`, `calibrada`, `duracao_s`,
`wer` (taxa de erro de palavra) e a `transcricao` que o Whisper ouviu.

## Como ler

`wer` × 13 dá os erros na frase: 0,077 é 1 erro em 13. A transcrição mostra
qual palavra o Whisper ouviu errado ("Cloud Code" no lugar de "Claude
Code", por exemplo).

## Números (19/10/2026)

| Voz | Modelo | Calibração nossa | Duração | Erros em 13 |
|---|---|---|---|---|
| dora | Kokoro-82M | sim (r10) | 4,67 s | 1 |
| alex | Kokoro-82M | sim (r10) | 4,74 s | 3 |
| santa | Kokoro-82M | não | 4,61 s | 3 |
| faber | Piper medium | não | 3,89 s | 3 |
| jeff | Piper medium | não | 5,14 s | 6 |
| cadu | Piper medium | não | 5,15 s | 8 |

## Fontes

1. Código e medida: https://github.com/peterwkdev-creator/tts-ptbr
2. Medida própria de 19/10/2026 (Whisper small, faster-whisper, CPU int8,
   beam 5).

## Limites e correções

- Uma frase, uma síntese por voz, uma data: outra frase pode dar outra
  ordem.
- O Whisper também erra: o que se mede é o que ele ouviu, não o que uma
  pessoa ouviria.
- "Calibração" é o método da versão r10 do TTS: dicionário de pronúncia,
  correção de fonemas e ritmo. As 4 sem calibração recebem a frase só com
  números e siglas por extenso (o normalizador, sem dicionário).
- O "Claude" não saiu certo em nenhuma das 6.
