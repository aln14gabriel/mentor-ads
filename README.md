# Monitor Didático de ADS — Projeto N2 (Startup de IA em Dupla)

MVP desenvolvido em Python para a disciplina de **Inteligência Artificial — Análise e Desenvolvimento de Sistemas (ADS)**, ministrada pela **Profª Tarciana**.

## 1. Problema e Solução

Estudantes iniciantes de Análise e Desenvolvimento de Sistemas frequentemente encontram mensagens de erro crípticas (em programação, banco de dados ou infraestrutura) e termos técnicos difíceis de interpretar na documentação oficial.

Este MVP atua como um **monitor didático por linha de comando (CLI)**: o aluno cola uma mensagem de erro ou dúvida técnica e recebe uma resposta estruturada em **JSON** contendo:

* **`conceito_ou_erro`**: identificação objetiva do tema ou erro;

* **`explicacao_simples`**: explicação clara em linguagem acessível em português (até 3 frases);

* **`analogia_cotidiano`**: comparação prática com situações do dia a dia;

* **`proximo_passo`**: sugestão prática de investigação, incentivando o aprendizado sem entregar código pronto de exercícios.

## 2. Arquitetura e Fluxo do MVP

```
Usuário (CLI) ──▶ app.py ──▶ llm.py (API compatível com OpenAI) ──▶ Resposta JSON parseada + Telemetria de Tokens + Aviso Ético
```

### Estrutura de Arquivos

* **`app.py`**: interface de entrada via terminal (`sys.argv` ou `input()`), exibição do JSON formatado, leitura rápida, contagem de tokens e aviso ético.

* **`llm.py`**: integração com a API de LLM (compatível com o SDK da OpenAI), suporte ao modo simulado (`LLM_MOCK=1`), parse de JSON (`json.loads`) e extração de métricas de tokens (`prompt_tokens`, `completion_tokens`, `total_tokens`).

* **`prompts.py`**: definição do `SYSTEM_PROMPT` separado da entrada do usuário, estabelecendo papel, regras pedagógicas e esquema JSON obrigatório.

* **`.env.example`**: modelo de variáveis de ambiente sem credenciais reais.

* **`.gitignore`**: garante que `venv/`, `__pycache__/`, `*.pyc` e o arquivo `.env` com a chave real não sejam versionados.

* **`requirements.txt`**: dependências do projeto (`openai`, `python-dotenv`, `pytest`).

## 3. Como Rodar o Projeto

### Pré-requisitos

* Python 3.10 ou superior instalado;

* Uma chave de API gratuita (ex.: Google AI Studio / Gemini Free Tier ou provedor compatível com OpenAI).

### Passo a passo

1. **Clone o repositório e acesse a pasta do projeto:**

   ```
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_PROJETO>
   ```

2. **Crie e ative um ambiente virtual:**

   * **Windows (PowerShell/CMD):**

     ```
     python -m venv venv
     venv\Scripts\activate
     ```

   * **Linux/macOS:**

     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instale as dependências:**

   ```
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   * **Windows:**

     ```
     copy .env.example .env
     ```

   * **Linux/macOS:**

     ```
     cp .env.example .env
     ```

   Edite o arquivo `.env`:

   * Para **teste local sem gastar tokens**, mantenha `LLM_MOCK=1`.

   * Para **execução real com a API**, altere para `LLM_MOCK=0` e preencha sua chave em `LLM_API_KEY`:

     ```
     LLM_MOCK=0
     LLM_API_KEY=sua_chave_real_aqui
     LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
     LLM_MODEL=gemini-3.5-flash-lite
     ```

5. **Execute a aplicação:**

   * Passando a dúvida ou erro diretamente como argumento:

     ```
     python app.py "OperationalError: no such table: usuarios"
     ```

   * Ou em modo interativo:

     ```
     python app.py
     ```

## 4. Exemplo de Saída e Demonstração (Prints / GIF)

> **\[INSIRA AQUI UM PRINT OU GIF DO TERMINAL EXECUTANDO O `app.py` EM MODO REAL (`LLM_MOCK=0`)\]**

Exemplo de saída gerada no terminal:

```
=== RESPOSTA ESTRUTURADA (JSON) ===
{
  "conceito_ou_erro": "Erro de tabela inexistente no SQLite (OperationalError)",
  "explicacao_simples": "O banco de dados tentou consultar ou gravar dados na tabela 'usuarios', mas ela ainda não foi criada ou o nome foi digitado diferente. Isso geralmente ocorre quando o script de criação do banco (CREATE TABLE) não foi executado antes da consulta.",
  "analogia_cotidiano": "É como tentar guardar uma pasta dentro de uma gaveta que ainda não foi montada no armário.",
  "proximo_passo": "Verifique se o comando CREATE TABLE usuarios foi executado com sucesso e se o arquivo de banco de dados conectado é o mesmo onde a tabela foi criada."
}

=== LEITURA RÁPIDA ===
Conceito/Erro: Erro de tabela inexistente no SQLite (OperationalError)
Explicação simples: ...
Analogia: ...
Próximo passo: ...

Tokens -> entrada: 185 | saída: 142 | total: 327

Aviso: Esta ferramenta utiliza IA para apoio didático em ADS e não substitui a orientação de um professor, monitor ou a documentação oficial.
```

## 5. Engenharia de Prompt e Controle de Tokens/Custo

* **Separação de papéis (`system` vs. `user`):** O contrato de comportamento e o esquema JSON ficam isolados em `prompts.py` (`SYSTEM_PROMPT`), enquanto a entrada do estudante é enviada exclusivamente no papel `user`.

* **Baixa temperatura (`temperature=0.3`):** Configurada para priorizar consistência estrutural na geração do JSON e precisão técnica nas explicações.

* **Limite de saída (`max_tokens=400`):** Evita respostas prolixas, reduz latência e controla o consumo de tokens de saída.

* **Modelo leve (`gemini-3.5-flash-lite`):** Escolhido pelo baixo custo e alta velocidade, operando dentro do *free tier*.

* **Telemetria em tempo real:** A cada chamada real, o sistema exibe no terminal `tokens_entrada`, `tokens_saida` e `tokens_total` retornados pelo objeto `usage` da API.

## 6. Ética, Privacidade e Limitações

* **Transparência e Apoio Educacional:** O sistema exibe explicitamente ao final de toda execução:

  > *"Aviso: Esta ferramenta utiliza IA para apoio didático em ADS e não substitui a orientação de um professor, monitor ou a documentação oficial."*

* **Integridade Acadêmica:** O `SYSTEM_PROMPT` instrui o modelo a indicar apenas o próximo passo de investigação, evitando gerar respostas prontas de provas ou trabalhos.

* **Risco de Alucinação:** Modelos de linguagem podem interpretar incorretamente erros muito específicos de ambiente ou bibliotecas recentes. Por isso, o usuário é sempre orientado a validar a sugestão na documentação oficial.

* **Dados Pessoais (LGPD) e Segurança:** Nenhuma entrada é armazenada em banco de dados pela aplicação. Recomenda-se que o usuário não cole senhas, tokens, strings de conexão com credenciais ou dados pessoais reais nas mensagens de erro. A chave da API permanece exclusivamente no `.env` local (ignorado pelo Git).

## 7. Declaração de Uso de IA

Em conformidade com as diretrizes da disciplina:

* Ferramentas de Inteligência Artificial generativa foram utilizadas como apoio durante o desenvolvimento deste projeto para estruturação inicial do código, revisão de documentação (`README.md`) e refinamento do `SYSTEM_PROMPT`.

* Todo o código foi revisado, testado e compreendido integralmente pelos integrantes da dupla, que estão aptos a explicar qualquer trecho durante a avaliação e o pitch.

## 8. Equipe e Contribuições

* **Alan Gabriel** — `<Responsabilidades, ex.: arquitetura da API, llm.py, testes de tokens>`

* **Maykoo Douglas** — `<Responsabilidades, ex.: engenharia de prompt, app.py, ética e documentação>`
