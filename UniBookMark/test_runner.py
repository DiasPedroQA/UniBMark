import random

def rodar_testes():
    """Simula testes e gera erros aleatórios"""
    erros = []
    erros.extend(
        f"Erro {i + 1}: Falha no módulo XYZ"
        for i in range(5)
        if random.choice([True, False])
    )
    return erros
