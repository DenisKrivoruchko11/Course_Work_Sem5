import portion

from src.main.backend.models.cyclogram import Cyclogram


def operation(x: Cyclogram, y: Cyclogram) -> Cyclogram:
    return Cyclogram('Title', ['1', '2', '3'], ['1', '2', '3'], 0, 10,
                     [[portion.empty() for _ in range(3)] for _ in range(3)])
