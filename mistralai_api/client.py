import logging

from mistralai import Mistral
from decouple import config

logger = logging.getLogger(__name__)

API_KEY = config('MISTRAL_KEY', default='')
MODEL = "mistral-small-latest"
TIMEOUT_MS = 10_000  # nao prender o request do usuario esperando a IA


def get_car_ai_bio(modelCar, brandCar, factoryYear):
    """Gera uma descricao de venda via Mistral.

    Retorna None quando a IA nao esta configurada ou falha: o cadastro do
    carro nunca deve quebrar por causa de uma dependencia externa.
    """
    if not API_KEY:
        logger.warning("MISTRAL_KEY nao configurada; pulando geracao de descricao.")
        return None

    prompt = f"""
Crie uma descrição de venda com no máximo 250 caracteres para o carro {brandCar} {modelCar} {factoryYear}.
A descrição deve ser realista e fluida, sem usar placeholders ou chaves.
Destaque pontos comuns desse modelo, como motor, conforto, tecnologia e design.
Não mencione a contagem de caractéres no final da mensagem.
Por favor não coloque caracteres especiais como aspas ou backticks no início ou fim da mensagem.
"""
    try:
        client = Mistral(api_key=API_KEY, timeout_ms=TIMEOUT_MS)
        chat_response = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7,
        )
        return chat_response.choices[0].message.content
    except Exception:
        logger.exception("Falha ao gerar descricao do carro pela Mistral.")
        return None
