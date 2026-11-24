import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def chamar_llm(system_prompt: str, user_prompt: str) -> dict:
    mock = os.getenv("LLM_MOCK", "1").strip() == "1"

    if mock:
        resposta_simulada = {
            "explicacao": (
                "Modo simulado ativo (LLM_MOCK=1): este trecho exemplifica como o Tutor ADS "
                "explica um código ou conceito de forma estruturada antes da chamada real à API."
            ),
            "quiz": {
                "pergunta": "Qual é a boa prática ao lidar com chaves de API no GitHub?",
                "opcoes": [
                    "A) Colar a chave direto no código principal",
                    "B) Guardar em .env (ignorado no .gitignore) e enviar apenas .env.example",
                    "C) Subir a chave em um arquivo txt público",
                    "D) Compartilhar a chave no README"
                ],
                "resposta_correta": "B",
                "justificativa": "Chaves são segredos e nunca devem ir para o repositório."
            },
            "aviso_educativo": (
                "Atenção: este conteúdo foi gerado por IA para apoio aos estudos e não substitui "
                "um professor ou profissional habilitado."
            )
        }
        return {
            "conteudo": json.dumps(resposta_simulada, ensure_ascii=False),
            "tokens_entrada": 0,
            "tokens_saida": 0,
            "tokens_total": 0,
            "modo": "simulado"
        }

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL") or None
    model = os.getenv("LLM_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise ValueError("LLM_API_KEY não encontrada no arquivo .env.")

    client = OpenAI(api_key=api_key, base_url=base_url)

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1200,
    )

    conteudo = resp.choices[0].message.content or ""
    usage = resp.usage

    tokens_entrada = getattr(usage, "prompt_tokens", 0) or 0
    tokens_saida = getattr(usage, "completion_tokens", 0) or 0
    tokens_total = getattr(usage, "total_tokens", 0) or (tokens_entrada + tokens_saida)

    return {
        "conteudo": conteudo,
        "tokens_entrada": tokens_entrada,
        "tokens_saida": tokens_saida,
        "tokens_total": tokens_total,
        "modo": "real"
    }
