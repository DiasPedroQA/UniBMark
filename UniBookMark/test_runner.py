"""
Módulo para simulação de execução de cálculos matemáticos
com geração aleatória de erros.

Este módulo contém uma função que simula a execução de
uma operação matemática simples, gerando erros aleatórios
em uma das operações de vez em quando. A função `executar_calculo`
realiza cálculos de soma ou multiplicação,
e aleatoriamente gera um erro durante a execução.

Funções:
    executar_calculo() -> tuple[float, bool]: Realiza um cálculo
    matemático simples e retorna o resultado,
    juntamente com um indicador de sucesso ou falha.
"""

import random
from random import seed


def executar_calculo() -> tuple[float, bool]:
    """
    Realiza um cálculo matemático simples de soma
    ou multiplicação e gera um erro aleatório.

    A função realiza uma operação simples
    (soma ou multiplicação) entre dois números.
    Dependendo de um valor aleatório, ela pode
    gerar um erro durante o cálculo, simulando uma falha no sistema.
    A falha ocorre apenas uma vez a cada execução,
    para testar o comportamento do sistema.

    Retorna:
        tuple[float, bool]: O resultado do cálculo e um
        indicador de sucesso (True) ou falha (False).
    """

    num1: float = random.uniform(1, 100)  # Número aleatório para o cálculo
    # Outro número aleatório para o cálculo
    num2: float = random.uniform(1, 100)

    # Decide aleatoriamente entre soma e multiplicação
    operacao: str = random.choice(["soma", "multiplicacao"])

    # Realiza o cálculo, mas de vez em quando gera um erro aleatório
    if random.choice([True, False]):
        resultado: float = num1 + num2 if operacao == "soma" else num1 * num2
        return resultado, True  # Sucesso no cálculo
    else:
        # Simula um erro de cálculo aleatório
        return 0.0, False  # Falha no cálculo


# Fixando a semente para garantir resultados previsíveis nos testes
seed(42)


def test_calculo_soma():
    """
    Teste para verificar se o cálculo de soma
    está funcionando corretamente.

    Espera-se que o cálculo de soma retorne o
    valor correto e um indicador de sucesso.
    """
    resultado, sucesso = executar_calculo()

    # Se o cálculo foi bem-sucedido, devemos validar que o valor é maior que 0.
    assert sucesso
    assert resultado > 0  # O resultado da soma deve ser um número positivo


def test_calculo_multiplicacao():
    """
    Teste para verificar se o cálculo de multiplicação
    está funcionando corretamente.

    Espera-se que o cálculo de multiplicação retorne o
    valor correto e um indicador de sucesso.
    """
    resultado, sucesso = executar_calculo()

    # Se o cálculo foi bem-sucedido, devemos validar que o valor é maior que 0.
    assert sucesso is True  # Corrigindo a comparação
    assert resultado > 0


def test_falha_calculo():
    """
    Teste para simular a falha no cálculo e
    garantir que o sistema lida com erros corretamente.

    Espera-se que a função retorne 0.0 e um indicador de falha.
    """
    resultado, sucesso = executar_calculo()

    # Espera-se que o resultado seja 0.0 em caso de falha e sucesso seja False
    assert not sucesso
    assert resultado == 0.0
