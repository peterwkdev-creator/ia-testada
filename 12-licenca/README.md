# 12-licenca: o código é MIT, o modelo não

Medida do post 12 da @peterwk.dev (a publicar): o repositório de um modelo
de IA pode ter uma licença e os pesos, outra. Aqui, para seis modelos, a
licença do código (GitHub) ao lado da licença dos pesos (Hugging Face), lidas
dos metadados públicos.

**Medido em 26/10/2026 (UTC)**, sem token e só com a biblioteca padrão do Python.

## O que mede

Para cada modelo, o `conferir_licencas.py` lê duas APIs:

- **código**: `GET https://api.github.com/repos/{dono}/{repo}`, campo
  `license.spdx_id` (vazio quando o repositório não declara licença);
- **pesos**: `GET https://huggingface.co/api/models/{id}`, campos
  `cardData.license` e `cardData.license_name` (na falta deles, a tag
  `license:...`).

A lógica que extrai a licença de um JSON já lido fica separada da rede, e os
testes (`tests/test_12_licenca.py`) a cobrem com JSON de exemplo, sem rede.

O F5-TTS diz isso no próprio README
(<https://github.com/SWivid/F5-TTS>): "Our code is released under MIT
License. The pre-trained models are licensed under the CC-BY-NC license due
to the training data Emilia".

O Kokoro, o Piper e o Whisper são os que o nosso TTS usa, pelo que o código
roda: do Kokoro, o `kokoro-onnx` (código) com os pesos do Kokoro-82M (os
arquivos `.onnx` dele são conversões desses pesos); do Whisper, o modelo
`small` pelo `faster-whisper`. O Piper só roda nas rodadas de comparação
de vozes, não na narração.

## Pré-requisitos

- Python 3.11 ou mais novo.
- Internet. Sem token: as APIs públicas limitam o número de pedidos por hora
  e por IP, e o script para com o erro se for barrado.

## Passo a passo

De dentro desta pasta (`cd 12-licenca`):

```bash
python -I conferir_licencas.py
```

Grava o [`medidas.tsv`](medidas.tsv) desta pasta, com a data UTC da coleta
em cada linha.

## Números (26/10/2026)

| Modelo | Licença do código (GitHub) | Licença dos pesos (Hugging Face) |
|---|---|---|
| F5-TTS | MIT | `cc-by-nc-4.0` |
| XTTS-v2 | MPL-2.0 | `other` (`coqui-public-model-license`) |
| LTX-2 | NOASSERTION (licença própria, sem identificador SPDX) | `other` (`ltx-2-community-license-agreement`) |
| Kokoro (kokoro-onnx) | MIT | `apache-2.0` |
| Piper (vozes) | GPL-3.0 | `mit` |
| Whisper (small) | MIT | `mit` |

Repositórios consultados: `SWivid/F5-TTS`, `idiap/coqui-ai-TTS`,
`Lightricks/LTX-2`, `thewh1teagle/kokoro-onnx`, `OHF-Voice/piper1-gpl` e
`SYSTRAN/faster-whisper`; pesos: `SWivid/F5-TTS`, `coqui/XTTS-v2`,
`Lightricks/LTX-2`, `hexgrad/Kokoro-82M`, `rhasspy/piper-voices` e
`Systran/faster-whisper-small`.

## Limites

- É a licença **declarada nos metadados**, não parecer jurídico: o texto da
  licença, as condições de uso e o que vale para o seu caso se leem na fonte.
- Um repositório e um id por modelo; um modelo pode ter outros repositórios
  e outras variantes de pesos, com licença diferente (no Whisper, só o
  `small` convertido para o `faster-whisper` foi consultado).
- As vozes pt_BR do Piper têm card próprio: dados CC0, afinadas a partir da
  voz lessac, cuja licença não conferimos; o `mit` é o do repositório.
- `NOASSERTION` e `other` não dizem qual é a licença: só que o GitHub não a
  reconheceu ou que o card aponta para um texto próprio.
- O Wav2Lip ficou de fora: não tem licença no GitHub nem card no Hugging Face.
- Os metadados mudam: a medida vale para a data acima.
