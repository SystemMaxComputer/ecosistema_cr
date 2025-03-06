import random
from .depredador import Depredador
from .presa import Presa
from .planta import Planta

class Ecosistema:
    def __init__(self, n, ciclos_maximos):
        self.n = n
        self.ciclos = 0
        self.ciclos_maximos = ciclos_maximos
        self.matriz = [[0] * n for _ in range(n)]
        self.llenar_matriz(0, 0)

    def llenar_matriz(self, x, y):
        if x >= self.n:
            return
        if y >= self.n:
            return self.llenar_matriz(x + 1, 0)

        prob = random.random()
        if prob < 0.2:
            self.matriz[x][y] = Depredador(energia=15)
        elif prob < 0.5:
            self.matriz[x][y] = Presa(energia=10)
        elif prob < 0.7:
            self.matriz[x][y] = Planta()

        self.llenar_matriz(x, y + 1)

    def mover_organismo(self, x, y, nuevo_x, nuevo_y):
        self.matriz[nuevo_x][nuevo_y] = self.matriz[x][y]
        self.matriz[x][y] = 0

    def ejecutar_ciclo(self):
        if self.ciclos >= self.ciclos_maximos:
            return "Simulación terminada"

        for x in range(self.n):
            for y in range(self.n):
                organismo = self.matriz[x][y]
                if isinstance(organismo, (Depredador, Presa)):
                    organismo.mover(self, x, y)
                    organismo.comer(self, x, y)

        self.ciclos += 1
        return self.ejecutar_ciclo()
print("Cargando ecosistema.py...")
