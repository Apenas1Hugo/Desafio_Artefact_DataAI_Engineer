
import os
import json

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from src.data.loader import load_data
from src.tools.products import search_products, get_product_price
from src.tools.orders import get_customer_orders
from src.tools.policies import search_policies



load_dotenv()


DATA = load_data()


def serialize_result(result) -> str:
    """Converte os resultados das ferramentas para JSON."""
    return json.dumps(result, ensure_ascii=False, default=str)




@tool
def product_search(query: str) -> str:
    """Busca instrumentos musicais disponíveis pelo nome, descrição ou categoria."""
    results = search_products(DATA, query)
    return serialize_result(results)


@tool
def product_price(product_id: int, payment_method: str = "credit") -> str:
    """Consulta o preço de um produto considerando promoções e forma de pagamento.
    payment_method aceita pix, credit ou debit.
    """
    result = get_product_price(DATA, product_id, payment_method)
    return serialize_result(result)


@tool
def customer_orders(customer_id: int) -> str:
    """Consulta os pedidos de um cliente pelo identificador interno."""
    result = get_customer_orders(DATA, customer_id)
    return serialize_result(result)


@tool
def store_policies(query: str) -> str:
    """Pesquisa as políticas da loja sobre pagamentos, trocas, garantia, frete e atendimento."""
    results = search_policies(query)
    return serialize_result(results)



TOOLS = [
    product_search,
    product_price,
    customer_orders,
    store_policies
]




def get_llm():
    """Inicializa o modelo de linguagem."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada no .env")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        groq_api_key=api_key,
        temperature=0
    )




def create_store_agent():
    """Cria o agente de atendimento com ferramentas e memória."""

    llm = get_llm()

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt="""
        Você é o assistente virtual da Empório da Música,
        uma loja de instrumentos musicais localizada em Campo Grande-MS.

        IDENTIDADE E ATENDIMENTO:
        - Responda sempre em português brasileiro.
        - Seja cordial, profissional e acolhedor.
        - Utilize uma linguagem natural, evitando respostas robóticas.

        UTILIZAÇÃO DAS FERRAMENTAS:
        - Utilize as ferramentas para consultar produtos, preços,
          pedidos e políticas da loja.
        - Não invente informações que deveriam ser consultadas.
        - Nunca invente preços, estoque, rastreamento ou prazos.
        - Não invente identificadores de clientes.

        REGRAS COMERCIAIS:
        - A loja comercializa exclusivamente instrumentos musicais.
        - Respeite as políticas comerciais retornadas pelas ferramentas.
        - Não prometa condições que não estejam documentadas.

        LIMITAÇÕES:
        - Se não encontrar informações suficientes, informe isso ao cliente.
        - Não invente políticas comerciais.
        - Quando necessário, recomende contato com atendimento humano.
        - Utilize somente informações presentes nos resultados das ferramentas ou nas instruções deste prompt.
        - Não invente especificações técnicas, características, recomendações ou condições comerciais.
        - Não deduza informações que não foram retornadas pelas ferramentas.
        - Ao apresentar produtos, utilize os nomes, preços, estoques e descrições fornecidos pela ferramenta.
        - Ao consultar pedidos, apresente somente os dados retornados pela ferramenta, sem acrescentar informações.
        - Não prometa trocas, reparos, reservas ou serviços que não estejam explicitamente documentados.
        - Se uma informação não estiver disponível, informe que não foi possível confirmá-la.
        """,
        checkpointer=checkpointer
    )

    return agent
