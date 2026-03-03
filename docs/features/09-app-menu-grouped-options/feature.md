# Feature: reorganizar menu por grupos com banner e limpeza de tela

## Objetivo
Reestruturar o menu do `app.py` para separar opcoes por grupos funcionais (`Lista`, `Usuario`, `Incidentes`).
Adicionar o banner `Skyhigh API` e limpar a tela sempre que uma opcao numerica for selecionada.

## Contexto
- Problema atual:
  - O menu esta linear e mistura acoes de dominios diferentes, dificultando navegacao e leitura no terminal.
- Motivacao:
  - Melhorar usabilidade, deixando o fluxo mais claro por contexto (lista, usuario e incidentes).

## Escopo
- Inclui:
  - Reorganizacao visual do menu em secoes:
    - `Lista`:
      - Validar a lista
      - Lista valores
      - Adicionar novo item
      - Deletar item
    - `Usuario`:
      - Criar
      - Deletar
      - Atualizar
      - Listar todos usuarios
    - `Incidentes`:
      - Listar
  - Exibicao de banner no topo: `Skyhigh API`.
  - Limpeza de tela ao entrar em qualquer opcao numerica do menu.
  - Manutencao das chamadas ja existentes no `WebClient`, alterando apenas fluxo de apresentacao/navegacao no `app.py`.
- Nao inclui:
  - Mudanca de contratos da API.
  - Novas operacoes fora das opcoes listadas acima.
  - Interface grafica.

## Implementação
1. Arquivos a criar/editar:
   - `app.py`
   - `docs/features/09-app-menu-grouped-options/feature.md`
2. Fluxo principal:
   - Renderizar banner `Skyhigh API` antes das opcoes.
   - Mostrar secoes do menu por grupo (`Lista`, `Usuario`, `Incidentes`) com numeracao unica.
   - Ao receber uma escolha numerica valida:
     - limpar terminal (`clear` no Linux/macOS ou `cls` no Windows);
     - exibir novamente o banner;
     - executar a acao correspondente.
   - Ao finalizar cada acao, retornar ao menu agrupado.
3. Dependências:
   - Sem novas dependencias externas; usar apenas biblioteca padrao para limpar tela.

## Critérios de aceitação
- [x] O menu exibe o banner `Skyhigh API` no topo.
- [x] As opcoes aparecem separadas por grupos `Lista`, `Usuario` e `Incidentes`.
- [x] O grupo `Lista` contem as opcoes de validar lista, listar valores, adicionar item e deletar item.
- [x] O grupo `Usuario` contem as opcoes de criar, deletar e atualizar.
- [x] O grupo `Usuario` contem tambem a opcao de listar todos usuarios.
- [x] O grupo `Incidentes` contem a opcao de listar.
- [x] Ao selecionar qualquer numero valido do menu, a tela e limpa antes de mostrar os novos dados.
- [x] O fluxo volta ao menu apos cada operacao sem encerrar a aplicacao indevidamente.

## Como executar/testar
```bash
source venv/bin/activate
python -m py_compile app.py
python app.py
# validar banner no topo
# validar secoes do menu por grupo
# selecionar diferentes numeros e confirmar limpeza de tela antes do resultado
```

## Riscos e observações
- Risco 1:
  - Limpeza de tela pode variar por sistema operacional se o comando nao for tratado por plataforma.
- Risco 2:
  - Mudanca de numeracao do menu pode quebrar referencias antigas de uso/manual se nao forem atualizadas.
- Observacao 1:
  - Recomenda-se centralizar o mapeamento de opcoes em estrutura unica para facilitar manutencao futura.
