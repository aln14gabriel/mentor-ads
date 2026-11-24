Mentor ADS — Projeto N2 (Startup de IA em Dupla)

MVP desenvolvido em Python para a disciplina de Inteligência Artificial — Análise e Desenvolvimento de Sistemas (ADS), ministrada pela Profª Tarciana.

1. Problema e Solução

Estudantes iniciantes de Análise e Desenvolvimento de Sistemas frequentemente encontram mensagens de erro crípticas (em programação, banco de dados ou infraestrutura) e termos técnicos difíceis de interpretar na documentação oficial, além de correrem o risco de usar IAs genéricas apenas para copiar respostas prontas.

Este MVP atua como um assistente didático por linha de comando (CLI) focado em aprendizado ativo: o aluno digita uma dúvida técnica ou cola um trecho de código e recebe uma resposta estruturada em JSON contendo:

explicacao: explicação didática, estruturada e objetiva do conceito ou código;

quiz: questão objetiva de fixação (pergunta, opcoes, resposta_correta e justificativa) para testar a compreensão real do tema;

aviso_educativo: lembrete explícito sobre o uso de Inteligência Artificial como apoio aos estudos, risco de alucinações e necessidade de validar com professores e documentação oficial.

2. Arquitetura e Fluxo do MVP

Usuário (CLI) ──▶ app.py ──▶ llm.py (API compatível com OpenAI) ──▶ JSON parseado + Explicação + Quiz + Telemetria de Tokens + Aviso Ético


Estrutura de Arquivos

app.py: interface de entrada via terminal (sys.argv ou input()), sanitização de blocos markdown (limpar_json), parse do JSON (json.loads), exibição da explicação, quiz, aviso educativo e contagem de tokens.

llm.py: integração com a API de LLM (compatível com o SDK da OpenAI), suporte ao modo simulado (LLM_MOCK=1) e modo real (LLM_MOCK=0), configuração de temperature=0.3 e max_tokens=1200, além da extração de métricas de tokens (prompt_tokens, completion_tokens, total_tokens).

prompts.py: definição do SYSTEM_PROMPT separado da entrada do usuário, estabelecendo papel pedagógico, guarda de escopo (apenas TI/ADS), proteção de privacidade e esquema JSON obrigatório.

.env.example: modelo de variáveis de ambiente sem credenciais reais.

.gitignore: garante que venv/, __pycache__/, *.pyc e o arquivo .env com a chave real não sejam versionados.

requirements.txt: dependências do projeto (openai, python-dotenv, pytest).

3. Como Rodar o Projeto

Pré-requisitos

Python 3.10 ou superior instalado;

Uma chave de API gratuita (ex.: Google AI Studio / Gemini Free Tier ou provedor compatível com OpenAI) para execução no modo real.

Passo a passo

Clone o repositório e acesse a pasta do projeto:

git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>


Crie e ative um ambiente virtual:

Windows (PowerShell/CMD):

python -m venv venv
venv\Scripts\activate


Linux/macOS / Git Bash:

python3 -m venv venv
source venv/bin/activate


Instale as dependências:

pip install -r requirements.txt


Configure as variáveis de ambiente:

Windows (CMD):

copy .env.example .env


Linux/macOS / Git Bash:

cp .env.example .env


Edite o arquivo .env:

Para teste local sem gastar tokens, mantenha LLM_MOCK=1.

Para execução real com a API, altere para LLM_MOCK=0 e preencha sua chave em LLM_API_KEY:

LLM_MOCK=0
LLM_API_KEY=sua_chave_real_aqui
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-3.5-flash-lite


Execute a aplicação:

Passando a dúvida ou código diretamente como argumento:

python app.py "Qual a diferença entre INNER JOIN e LEFT JOIN em SQL?"


Ou em modo interativo:

python app.py


4. Exemplo de Saída e Demonstração (Prints / GIF)

[INSIRA AQUI UM PRINT OU GIF DO TERMINAL EXECUTANDO O app.py EM MODO REAL (LLM_MOCK=0)]

Exemplo de saída gerada no terminal:

=== EXPLICAÇÃO ===
O INNER JOIN retorna apenas os registros que possuem correspondência nas duas tabelas relacionadas. Já o LEFT JOIN retorna todos os registros da tabela à esquerda (principal), preenchendo com NULL os campos da tabela à direita quando não houver correspondência.

=== QUIZ ===
Em uma consulta entre as tabelas 'Clientes' (esquerda) e 'Pedidos' (direita), qual comando lista todos os clientes, inclusive aqueles que nunca fizeram pedidos?
  A) INNER JOIN Pedidos ON Clientes.id = Pedidos.cliente_id
  B) LEFT JOIN Pedidos ON Clientes.id = Pedidos.cliente_id
  C) RIGHT JOIN Clientes ON Clientes.id = Pedidos.cliente_id
  D) CROSS JOIN Clientes
Resposta correta: B) LEFT JOIN Pedidos ON Clientes.id = Pedidos.cliente_id
Justificativa: O LEFT JOIN preserva todas as linhas da tabela à esquerda ('Clientes'), mesmo sem correspondência em 'Pedidos'. As demais opções filtram clientes sem pedidos ou invertem a lógica da relação.

=== AVISO ===
Aviso: conteúdo gerado por Inteligência Artificial para apoio aos estudos em ADS. Pode conter imprecisões (alucinações) e não substitui a orientação de professores ou documentação oficial.

=== TOKENS / MODO ===
Modo: real | Entrada: 295 | Saída: 210 | Total: 505


5. Engenharia de Prompt e Controle de Tokens/Custo

Separação de papéis (system vs. user): O contrato de comportamento, a guarda de escopo e o esquema JSON ficam isolados em prompts.py (SYSTEM_PROMPT), enquanto a dúvida ou trecho de código do estudante é enviado exclusivamente no papel user.

Baixa temperatura (temperature=0.3): Configurada para priorizar consistência estrutural na geração do JSON e precisão técnica nas explicações.

Limite de saída (max_tokens=1200): Dimensionado para comportar a explicação detalhada e o quiz completo com justificativa sem truncar o JSON, mantendo o custo controlado.

Modelo leve (gemini-3.5-flash-lite): Escolhido pelo baixo custo e alta velocidade, operando dentro do free tier.

Tratamento de resposta e contingência (LLM_MOCK): A função limpar_json remove eventuais cercas markdown antes do json.loads, com tratamento de JSONDecodeError no app.py. O modo LLM_MOCK=1 permite validar todo o fluxo sem consumir cota da API.

Telemetria em tempo real: A cada chamada, o sistema exibe no terminal o modo de execução e os tokens de entrada, saída e total retornados pelo objeto usage da API.

6. Ética, Privacidade e Limitações

Transparência e Apoio Educacional: O sistema exibe explicitamente ao final de toda execução o campo aviso_educativo:

"Aviso: conteúdo gerado por Inteligência Artificial para apoio aos estudos em ADS. Pode conter imprecisões (alucinações) e não substitui a orientação de professores ou documentação oficial."

Aprendizado Ativo: O SYSTEM_PROMPT instrui o modelo a explicar a lógica passo a passo e propor um quiz de fixação, evitando entregar respostas prontas sem explicação.

Guarda de Escopo e Segurança de Prompt: Consultas fora de TI/ADS ou tentativas de sobrescrever as instruções do sistema são recusadas educadamente dentro da própria estrutura JSON.

Risco de Alucinação: Modelos de linguagem podem interpretar incorretamente erros muito específicos de ambiente ou bibliotecas recentes. Por isso, o usuário é sempre orientado a validar o resultado na documentação oficial e com o professor.

Dados Pessoais (LGPD) e Segurança: Nenhuma entrada é armazenada em banco de dados pela aplicação, e o próprio prompt instrui o modelo a alertar o usuário caso ele cole dados pessoais sensíveis (CPFs, senhas ou chaves reais). A LLM_API_KEY permanece exclusivamente no .env local (ignorado pelo Git).

7. Declaração de Uso de IA

Em conformidade com as diretrizes da disciplina:

Ferramentas de Inteligência Artificial generativa foram utilizadas como apoio durante o desenvolvimento deste projeto para estruturação inicial do código, revisão de documentação (README.md) e refinamento do SYSTEM_PROMPT.

Todo o código foi revisado, testado e compreendido integralmente pelos integrantes da dupla, que estão aptos a explicar qualquer trecho durante a avaliação e o pitch.

8. Equipe e Contribuições

Alan Gabriel — Arquitetura e integração com a API (llm.py), tratamento de JSON e fluxo CLI (app.py), telemetria de tokens e testes de execução.

Maykoo Douglas — Engenharia do SYSTEM_PROMPT e regras de escopo (prompts.py), diretrizes éticas/LGPD, revisão de conformidade e documentação (README.md).
