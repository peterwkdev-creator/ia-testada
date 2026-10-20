# Como contribuir

Mediu e deu diferente: abra uma issue pelo modelo "Resultado diferente do
medido". É a contribuição mais útil daqui: cada medida vale para um
computador, uma sessão e uma data, e a sua pode mostrar o que mudou. Ideia,
medida que falta ou dúvida: pelo modelo "Sugestão ou dúvida". Para mandar
código:

- Os testes rodam do checkout, sem dependência fora da biblioteca padrão do
  Python:

  ```bash
  python -m unittest
  ```

- Dependência externa precisa de motivo no pull request.
- Todo medidor tem teste com dados inventados e o resultado esperado escrito
  à mão no próprio teste.
- Medida nova ou refeita entra com a data, a versão do que foi medido, a
  fonte com URL, o comando para refazer e os limites, no README da pasta.
- Nada de dado privado: nem transcrição de sessão, nem caminho com id da
  conta, nem e-mail ou token. O medidor grava só o que a tabela mostra.
- Código, mensagens e documentação em português do Brasil.
- Mudança de medida ou de comportamento entra no [CHANGELOG.md](CHANGELOG.md).
- Código próprio: não traga código copiado de outro projeto, mesmo de
  licença livre. O que você contribui sai sob a [licença MIT](LICENSE) do
  projeto.
