import re

# Expressões regulares para identificar caminhos
REGEX_CAMINHO_ABSOLUTO = re.compile(
    r"^(?:[A-Z]:\\|/|\w+:/).*", re.IGNORECASE
)  # Windows & Unix
REGEX_CAMINHO_RELATIVO = re.compile(r"^(?![A-Z]:\\|/|\w+:).+")  # Caminho relativo
