from classes import Pratica
from visual import visualize
from pathlib import Path

if __name__ == "__main__":
    pratiche = Path("pratiche")
    for p in pratiche.glob("*"):
        pratica = Pratica(p)
        visualize(pratica)