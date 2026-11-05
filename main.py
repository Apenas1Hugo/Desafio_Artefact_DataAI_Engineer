
import uuid

from src.agent import create_store_agent


def main():
    print("=" * 50)
    print(" EMPÓRIO DA MÚSICA - ASSISTENTE VIRTUAL")
    print("=" * 50)

    try:
        agent = create_store_agent()
    except Exception as error:
        print(f"Erro ao inicializar o agente: {error}")
        return

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    print("\nAssistente: Olá! Como posso ajudar?")
    print("Digite 'sair' para encerrar o atendimento.\n")

    while True:
        try:
            user_input = input("Você: ").strip()

            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\nAssistente: Obrigado pelo contato! Até logo.")
                break

            if not user_input:
                continue

            response = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                },
                config=config
            )

            answer = response["messages"][-1].content

            if isinstance(answer, list):
                answer = "\n".join(
                    block["text"]
                    for block in answer
                    if isinstance(block, dict) and "text" in block
                )

            print(f"\nAssistente: {answer}\n")

        except KeyboardInterrupt:
            print("\n\nAtendimento encerrado.")
            break

        except Exception as error:
            print(f"\nErro durante o atendimento: {error}\n")


if __name__ == "__main__":
    main()
