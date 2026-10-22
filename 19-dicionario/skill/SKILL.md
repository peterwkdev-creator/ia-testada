---
name: programar-post
description: Roteiro enxuto para programar um Reel pronto da peterwk.dev no FB e no IG (Meta Business Suite) e no TikTok (Studio), com orçamento de passos, o que funcionou e o que não fazer. Usar sempre que for programar, agendar ou subir um post nas redes.
---

# Programar um post nas 3 redes

Medido em 22/10 (post 30): 8 sessões, 478 passos, 252 no navegador (FB 86,
IG 77, TikTok 41) para um trabalho de ~36. Causas, em ordem: legenda do IG
por `insertText`/`selectAll` (~45), "Personalizar post" com campo único
(~40), capturas de tela para conferir (~45), recomeços depois de limpar no
meio do composer (~20), seletor de hora (~18), sim do Peter perdido no
/clear (6 barradas). Este roteiro corta cada uma.

## Antes de abrir o navegador (1 passo de shell + 1 pergunta)

1. Num comando só: caminho do MP4 e sha256; as legendas FB, IG e TikTok
   do `roteiro.md` do post; para cada uma, tamanho sem espaços e sha256 do
   texto sem espaços (é a conferência no fim); a 1ª linha de cada.
2. **Um `AskUserQuestion` só** com o sim para as 3 redes: data, hora,
   arquivo e qual legenda. O sim vale nesta sessão; não atravessa /clear.
3. **Orçamento:** ~12 chamadas por rede, ~40 no total com a conferência.
   Se a sessão já passou de 15 passos, limpar **antes** de abrir o
   composer, nunca no meio (recomeçar o composer custa mais que a limpeza).

## Como agir na tela

- Pensar a sequência inteira antes do lote; um `browser_batch` por etapa,
  terminando numa leitura por texto (`find`, `get_page_text` ou JS que
  devolve só o que importa).
- Captura de tela só quando a leitura por texto falhar, com `scale` ≤ 0,2.
- Errou no meio: não remendar. Descartar e refazer a etapa do zero.
- Sair do composer: Cancelar > "Descartar alterações" antes de navegar
  (senão "Leave site?" trava a aba).

## Upload de vídeo (Business Suite; o Studio aceita o mesmo truque)

`javascript_tool`, depois `find` "#pkd-file" e `file_upload`:

```js
const orig=HTMLInputElement.prototype.click;HTMLInputElement.prototype.click=function(){if(this.type==='file'){this.id='pkd-file';if(!this.isConnected){this.style.display='none';document.body.appendChild(this);}return;}return orig.call(this);};const b=[...document.querySelectorAll('[role="button"],button')].find(x=>x.innerText.trim()==='Adicionar vídeo');b.click();await new Promise(r=>setTimeout(r,800));HTMLInputElement.prototype.click=orig;const f=document.getElementById('pkd-file');JSON.stringify({found:!!f,accept:f&&f.accept})
```

Esperar 100% antes da legenda (vídeo primeiro, sempre).

## FB (Business Suite)

URL: `https://business.facebook.com/latest/reels_composer?asset_id=0000000000000000&business_id=0000000000000000`

1. "Postar em": **só a Página**. FB e IG são **dois posts separados**;
   nunca "Personalizar post" (as abas usam o mesmo campo).
2. Vídeo (acima). 3. Legenda FB: `execCommand('insertText')` serve aqui.
4. Avançar até Compartilhar > Programar; data no campo; hora nos
   **spinbuttons "horas" e "minutos" à parte** (clicar em cada, digitar
   12 e 00; "1200" num campo dá hora errada).
5. Conferir legenda (sem espaços + hash), data e hora por texto.
6. Clique final "Programar" (o sim pedido no início já cobre; se o modo auto
   barrar, manual no próprio clique e de volta ao auto).

## IG (Business Suite, outro post)

Mesma URL. "Postar em": só o IG (Página desmarcada). Vídeo primeiro.
Legenda: **clique real** no campo "Legenda do reel" e **digitar linha a
linha** num lote (`type` de cada linha, `Enter` em cada quebra, hashtags no
fim, `Escape`). **Nunca** `insertText` (troca a 1ª linha e derruba o
editor) nem `ctrl+a`/`selectAll` + apagar (derruba o editor). Avançar pula
o Editar e cai em Compartilhar; data e hora como no FB; conferir; Programar.
Rótulo de IA: o Business Suite não tem; liga-se no instagram.com depois
que o post sai (Editar > chave > Concluir), com o sim do Peter.

## TikTok (Studio)

URL: `https://www.tiktok.com/tiktokstudio/upload`

1. Vídeo pelo input da página (ou o truque acima). Esperar o envio.
2. Descrição (Draft.js): clique no editor, `ctrl+a`, `Delete` pelo
   teclado; **digitar a 1ª linha** (`type`) e `Enter Enter`; o resto por
   `ClipboardEvent('paste')` com `DataTransfer`. Colar tudo perde a 1ª
   linha às vezes; digitar tudo perde parágrafos. Conferir o 1º bloco e o
   total sem espaços.
3. "Exibir mais" > "Conteúdo gerado por IA" ligado; sem localização.
4. Programar: data; hora pelo `.tiktok-timepicker-option-text`: o campo
   no pé da tela (`scrollIntoView({block:'end'})`), abre **para cima** e
   tarda ~1 s; esperar e clicar **pela posição** da opção (clique por
   script não pegou). Conferir os `input` de texto: "12:00".
5. "Agendar".

## Fim (2 leituras + registro)

- Planner (`https://business.facebook.com/latest/planner?asset_id=0000000000000000&business_id=0000000000000000`)
  por texto: o dia, a hora, FB e IG. TikTok: `tiktokstudio/content`, a
  linha "dd de mês, hh:mm".
- Uma linha no "Onde retomar" (`progress.md`) e o detalhe em
  `progress/perfil.md`; commit com o sim do Peter.
- Algo novo que falhou ou funcionou: corrigir **este arquivo**, não só o
  progress (a receita espalhada em 4 arquivos foi metade do retrabalho).
