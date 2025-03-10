"""
Módulo para simulação de execução de testes com geração aleatória de erros.

Este módulo contém uma função que simula a execução de testes de software e
gera erros aleatórios. A função `rodar_testes` simula falhas nos módulos de
um sistema, criando mensagens de erro fictícias para testar o comportamento
do sistema de forma controlada.

Funções:
    rodar_testes() -> List[str]: Simula a execução de testes e retorna uma
    lista de erros aleatórios.
"""

import random


def rodar_testes() -> list[str]:
    """
    Simula a execução de testes e gera erros aleatórios.

    Esta função cria uma lista de erros simulados, onde cada erro é uma
    mensagem indicando a falha em um módulo específico do sistema. A
    geração de erros é aleatória e o número de erros varia a cada execução.

    Retorna:
        List[str]: Uma lista de strings contendo mensagens de erro
        geradas aleatoriamente.
    """
    erros: list[str] = []  # Lista para armazenar as mensagens de erro

    # Gera erros aleatórios, de 0 a 5 erros
    erros.extend(
        f"Erro {i + 1}: Falha no módulo XYZ"
        for i in range(5)
        if random.choice([True, False])
    )

    return erros
