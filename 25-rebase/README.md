# 25-rebase: quando o push forçado apaga o commit do colega

Medida do post 25 da @peterwk.dev (a publicar): o rebase reescreve o
histórico, e o push forçado que vem depois pode apagar do remoto o commit
que um colega acabou de empurrar. Aqui, com git de verdade e sem IA, quatro
jeitos de forçar o push e o que sobra no remoto.

**Medido em 23/10/2026, com o git 2.56.0**, no Windows.

## O que mede

Cada cenário monta numa pasta temporária um remoto bare e dois clones (você
e o colega) da mesma branch `feature`. O colega empurra um commit; você,
sem saber, reescreve o seu (`commit --amend`, como num rebase) e força o
push. O `medir_rebase.py` grava se o push foi aceito e se o commit do
colega continua na `feature` do remoto. A configuração global e a do
sistema ficam de fora (`GIT_CONFIG_GLOBAL` e `GIT_CONFIG_NOSYSTEM`), para o
resultado não depender da máquina.

## Pré-requisitos

- Python 3.11 ou mais novo.
- Git 2.30 ou mais novo (o `--force-if-includes` entrou no 2.30).

## Passo a passo

De dentro desta pasta (`cd 25-rebase`):

```bash
python -I medir_rebase.py
```

Grava o [`medidas.tsv`](medidas.tsv) desta pasta, com a versão do git na
última linha. Não usa rede: tudo fica na pasta temporária, apagada no fim.

## Números (23/10/2026)

| Push | `fetch` antes | Resultado | Commit do colega no remoto |
|---|---|---|---|
| `--force` | não | aceito | **apagado** |
| `--force-with-lease` | não | barrado | fica |
| `--force-with-lease` | sim | aceito | **apagado** |
| `--force-with-lease --force-if-includes` | sim | barrado | fica |

O `--force-with-lease` sozinho só protege enquanto você não faz `fetch`:
o `fetch` atualiza a referência que ele compara, e o push passa. O
`--force-if-includes` confere também se o commit do remoto está no seu
histórico, e barra.

## Limites

- Um colega, um commit e uma branch; sem servidor de verdade (GitHub,
  GitLab), onde regras de proteção da branch podem barrar antes.
- O `fetch` daqui é o comando explícito; um editor que faz `fetch` sozinho
  em segundo plano cai no 3º cenário sem você ver.
