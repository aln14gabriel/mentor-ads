# Tutor ADS — Assistente de Estudos com IA Generativa

MVP em Python de um assistente didático voltado a estudantes de **Análise e Desenvolvimento de Sistemas (ADS)** para explicar conceitos e trechos de código, gerar um quiz de fixação e exibir avisos educativos com transparência no consumo de tokens.

---

## 1. Problema e Proposta de Valor

Estudantes iniciantes e intermediários de ADS frequentemente travam em conceitos fundamentais (como modelagem relacional, consultas SQL, lógica de programação e orientação a objetos) ou não têm retorno imediato ao tentar revisar um trecho de código fora do horário de aula.

O **Tutor ADS** resolve esse problema oferecendo um fluxo rápido via linha de comando que:
- Explica o conceito ou código de forma didática e focada em TI/ADS.
- Mantém o escopo mesmo diante de perguntas fora do tema ou solicitações vagas.
- Gera uma questão de múltipla escolha (quiz) com resposta correta e justificativa para consolidar o aprendizado.
- Exibe um aviso educativo explícito e registra o consumo de tokens da requisição.

---

## 2. Arquitetura e Estrutura do Projeto

```text
tutor-ads-ia/
├── app.py            # Entrada via CLI, orquestração do fluxo e exibição formatada
├── llm.py            # Integração com a API (OpenAI-compatible / Google AI Studio) e modo mock
├── prompts.py        # Definição de system prompt, regras de escopo e estrutura JSON
├── .env.example      # Modelo de variáveis de ambiente (sem segredos reais)
├── .gitignore        # Garante que .env, venv/ e arquivos temporários não vão ao Git
├── requirements.txt  # Dependências Python do projeto
└── README.md         # Documentação técnica e guia de uso
