import random

def rodar_testes():
    """Simula testes e gera erros aleatórios"""
    erros = []
    for i in range(5):  # Simula 5 testes
        if random.choice([True, False]):  # 50% de chance de erro
            erros.append(f"Erro {i+1}: Falha no módulo XYZ")
    return erros
