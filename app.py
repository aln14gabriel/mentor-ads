import json
import sys
from llm import chamar_llm
from prompts import SYSTEM_PROMPT


def limpar_json(texto: str) -> str:
    limpo = texto.strip()
    if limpo.startswith("```"):
        linhas = limpo.splitlines()
        if linhas and linhas[0].startswith("```"):
            linhas = linhas[1:]
        if linhas and linhas[-1].strip() == "```":
            linhas = linhas[:-1]
        limpo = "\n".join(linhas).strip()
    return limpo


def main():
    if len(sys.argv) > 1:
        pergunta = " ".join(sys.argv[1:])
    else:
        pergunta = input("Digite sua dúvida de ADS ou cole um trecho de código: ").strip()

    if not pergunta:
        print("Nenhuma dúvida informada.")
        return

    try:
        resultado = chamar_llm(SYSTEM_PROMPT, pergunta)
        json_bruto = limpar_json(resultado["conteudo"])
        dados = json.loads(json_bruto)

        print("\n=== EXPLICAÇÃO ===")
        print(dados.get("explicacao", ""))

        quiz = dados.get("quiz", {})
        print("\n=== QUIZ ===")
        print(quiz.get("pergunta", ""))
        for opcao in quiz.get("opcoes", []):
            print(" ", opcao)
        print("Resposta correta:", quiz.get("resposta_correta", ""))
        print("Justificativa:", quiz.get("justificativa", ""))

        print("\n=== AVISO ===")
        print(dados.get("aviso_educativo", ""))

        print("\n=== TOKENS / MODO ===")
        print(
            f"Modo: {resultado['modo']} | Entrada: {resultado['tokens_entrada']} | "
            f"Saída: {resultado['tokens_saida']} | Total: {resultado['tokens_total']}"
        )

    except json.JSONDecodeError:
        print("\nErro: a resposta da IA não veio em JSON válido.")
        print("Resposta recebida:\n", resultado.get("conteudo", ""))
    except Exception as e:
        print(f"\nErro ao executar: {e}")


if __name__ == "__main__":
    main()
