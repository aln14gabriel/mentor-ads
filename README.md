# Mentor ADS — Projeto (Startup de IA em Dupla)

MVP desenvolvido em Python para a disciplina de **Inteligência Artificial — Análise e Desenvolvimento de Sistemas (ADS)**, ministrada pela **Profª Tarciana**.

## 1. Problema e Solução

Estudantes iniciantes de Análise e Desenvolvimento de Sistemas frequentemente encontram mensagens de erro crípticas (em programação, banco de dados ou infraestrutura) e termos técnicos difíceis de interpretar na documentação oficial.

Este MVP atua como um **monitor didático por linha de comando (CLI)**: o aluno cola uma mensagem de erro ou dúvida técnica e recebe uma resposta estruturada em **JSON** contendo:

- **`conceito_ou_erro`**: identificação objetiva do tema ou erro;
- **`explicacao_simples`**: explicação clara em linguagem acessível em português (até 3 frases);
- **`analogia_cotidiano`**: comparação prática com situações do dia a dia;
- **`proximo_passo`**: sugestão prática de investigação, incentivando o aprendizado sem entregar código pronto de exercícios ou provas.

## 2. Arquitetura e Fluxo do MVP

```text
Usuário (CLI) ──▶ app.py ──▶ llm.py (API compatível com OpenAI) ──▶ Resposta JSON parseada + Telemetria de Tokens + Aviso Ético
```

### Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `app.py` | Interface de entrada via terminal (`sys.argv` ou `input()`), exibição do JSON formatado, leitura rápida, contagem de tokens e aviso ético. |
| `llm.py` | Integração com a API de LLM (compatível com o SDK da OpenAI), suporte ao modo simulado (`LLM_MOCK=1`), parse de JSON (`json.loads`) e extração de métricas de tokens (`prompt_tokens`, `completion_tokens`, `total_tokens`). |
| `prompts.py` | Definição do `SYSTEM_PROMPT` separado da entrada do usuário, estabelecendo papel, regras pedagógicas, guarda de escopo e esquema JSON obrigatório. |
| `.env.example` | Modelo de variáveis de ambiente sem credenciais reais. |
| `.gitignore` | Garante que `venv/`, `__pycache__/`, `*.pyc` e o arquivo `.env` com a chave real não sejam versionados. |
| `requirements.txt` | Dependências do projeto (`openai`, `python-dotenv` e demais pacotes necessários para o CLI). |

## 3. Como Rodar o Projeto

### Pré-requisitos

- Python 3.10 ou superior instalado;
- Uma chave de API gratuita (ex.: Google AI Studio / Gemini Free Tier ou provedor compatível com OpenAI) para execução no modo real.

### Passo a passo

**1. Clone o repositório e acesse a pasta do projeto:**

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

**2. Crie e ative um ambiente virtual:**

Git Bash (Windows):

```bash
python -m venv venv
source venv/Scripts/activate
```

PowerShell / CMD (Windows):

```bat
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**

Git Bash / Linux / macOS:

```bash
cp .env.example .env
```

PowerShell / CMD:

```bat
copy .env.example .env
```

**5. Edite o arquivo `.env`:**

- Para teste local rápido, sem gastar tokens ou sem internet, mantenha `LLM_MOCK=1`.
- Para execução real com a API, altere para `LLM_MOCK=0` e preencha sua chave em `LLM_API_KEY`:

```env
LLM_MOCK=0
LLM_API_KEY=sua_chave_real_aqui
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-3.5-flash-lite
```

**6. Execute a aplicação:**

Passando a dúvida ou erro diretamente como argumento:

```bash
python app.py "Qual a diferença entre chave primária e chave estrangeira em SQL?"
```

Ou em modo interativo:

```bash
python app.py
```

## 4. Exemplo de Saída e Demonstração (Prints / GIF)

> **[INSIRA AQUI UM PRINT OU GIF DO TERMINAL EXECUTANDO O `app.py` EM MODO REAL (`LLM_MOCK=0`)]**

Exemplo de saída gerada no terminal:

```text
=== RESPOSTA ESTRUTURADA (JSON) ===
{
  "conceito_ou_erro": "Chave Primária (PRIMARY KEY) vs. Chave Estrangeira (FOREIGN KEY) em SQL",
  "explicacao_simples": "A chave primária identifica de forma única cada registro de uma tabela e não aceita valores nulos. Já a chave estrangeira cria o relacionamento entre tabelas apontando para a chave primária de outra tabela.",
  "analogia_cotidiano": "É como o número de matrícula de um aluno na secretaria ser a chave primária, e esse mesmo número constar na lista de presença da turma como chave estrangeira.",
  "proximo_passo": "Teste criar duas tabelas relacionadas (como 'alunos' e 'matriculas') no SQL e observe o que acontece ao tentar inserir uma matrícula para um aluno que não existe."
}

=== LEITURA RÁPIDA ===
Conceito/Erro: Chave Primária (PRIMARY KEY) vs. Chave Estrangeira (FOREIGN KEY) em SQL
Explicação simples: A chave primária identifica de forma única cada registro de uma tabela e não aceita valores nulos...
Analogia: É como o número de matrícula de um aluno na secretaria...
Próximo passo: Teste criar duas tabelas relacionadas...

Tokens -> entrada: 185 | saída: 142 | total: 327

Aviso: Esta ferramenta utiliza IA para apoio didático em ADS e não substitui a orientação de um professor, monitor ou a documentação oficial.
```

## 5. Engenharia de Prompt e Controle de Tokens/Custo

- **Separação de papéis (system vs. user):** o contrato de comportamento, o foco em TI/ADS e o esquema JSON ficam isolados em `prompts.py` (`SYSTEM_PROMPT`), enquanto a dúvida ou erro do estudante é enviada exclusivamente no papel `user`.
- **Baixa temperatura (`temperature=0.3`):** configurada para priorizar consistência estrutural na geração do JSON e precisão técnica nas explicações.
- **Limite de saída (`max_tokens=400`):** evita respostas prolixas, reduz latência e controla o consumo de tokens de saída.
- **Contingência com `LLM_MOCK`:** permite validar o fluxo do CLI mesmo sem chave de API, sem cota disponível ou sem conexão durante testes e apresentações.
- **Telemetria em tempo real:** a cada chamada real, o sistema exibe no terminal os tokens de entrada, saída e total retornados pela API.

## 6. Ética, Privacidade e Limitações

- **Transparência e Apoio Educacional:** o sistema exibe explicitamente ao final de toda execução:

  > "Aviso: Esta ferramenta utiliza IA para apoio didático em ADS e não substitui a orientação de um professor, monitor ou a documentação oficial."

- **Integridade Acadêmica:** o `SYSTEM_PROMPT` orienta o modelo a explicar o conceito e indicar o próximo passo de investigação, evitando entregar respostas prontas de atividades ou provas.
- **Risco de Alucinação:** modelos de linguagem podem interpretar incorretamente mensagens de erro muito específicas ou mudanças recentes de versões. Por isso, o estudante deve sempre conferir o resultado na documentação oficial e com o professor.
- **Dados Pessoais (LGPD) e Segurança:** nenhuma entrada é armazenada em banco de dados pela aplicação. Recomenda-se que o usuário não cole senhas, tokens, credenciais ou dados pessoais reais nas consultas. A `LLM_API_KEY` fica apenas no `.env` local, ignorado pelo Git.

## 7. Declaração de Uso de IA

Em conformidade com as diretrizes da disciplina:

- Ferramentas de Inteligência Artificial generativa foram utilizadas como apoio durante o desenvolvimento deste projeto para estruturação inicial do código, revisão de documentação (`README.md`) e refinamento do `SYSTEM_PROMPT`.
- Todo o código foi revisado, testado e compreendido integralmente pelos integrantes da dupla, que estão aptos a explicar qualquer trecho durante a avaliação e o pitch.

## 8. Equipe e Contribuições

| Integrante | Contribuições |
|---|---|
| **Alan Gabriel** | Integração com a API (`llm.py`), configuração de ambiente/telemetria de tokens e testes de execução no CLI. |
| **Maykoo Douglas** | Interface CLI (`app.py`), engenharia do `SYSTEM_PROMPT` (`prompts.py`), diretrizes éticas/LGPD e documentação. |
