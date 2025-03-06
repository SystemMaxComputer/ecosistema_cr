import random

class Planta:
    def __init__(self):
        self.tipo = "Planta"

class Depredador:
    def __init__(self, energia):
        self.energia = energia
        self.tipo = "Depredador"

    def mover(self, ecosistema, x, y):
        print(f"🔵 Depredador en ({x},{y}) intenta moverse")
        presa_x, presa_y = self.buscar_presa(ecosistema, x, y)
        if presa_x is not None and presa_y is not None:
            print(f"⚡ Depredador se mueve hacia la presa en ({presa_x},{presa_y})")
            ecosistema.mover_organismo(x, y, presa_x, presa_y)
        else:
            print("🚶 Depredador se mueve aleatoriamente")
            self.mover_aleatorio(ecosistema, x, y)

    def buscar_presa(self, ecosistema, x, y):
        return self.buscar_presa_recursivo(ecosistema, x, y, 0, 1) or \
               self.buscar_presa_recursivo(ecosistema, x, y, 0, -1) or \
               self.buscar_presa_recursivo(ecosistema, x, y, 1, 0) or \
               self.buscar_presa_recursivo(ecosistema, x, y, -1, 0)

    def buscar_presa_recursivo(self, ecosistema, x, y, dx, dy):
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < ecosistema.n and 0 <= nuevo_y < ecosistema.n:
            if isinstance(ecosistema.matriz[nuevo_x][nuevo_y], Presa):
                return nuevo_x, nuevo_y
            return self.buscar_presa_recursivo(ecosistema, nuevo_x, nuevo_y, dx, dy)
        return None, None

    def mover_aleatorio(self, ecosistema, x, y):
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcciones)
        self.mover_aleatorio_recursivo(ecosistema, x, y, direcciones, 0)

    def mover_aleatorio_recursivo(self, ecosistema, x, y, direcciones, i):
        if i == len(direcciones):
            return

        dx, dy = direcciones[i]
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < ecosistema.n and 0 <= nuevo_y < ecosistema.n and ecosistema.matriz[nuevo_x][nuevo_y] == 0:
            ecosistema.mover_organismo(x, y, nuevo_x, nuevo_y)
            return

        self.mover_aleatorio_recursivo(ecosistema, x, y, direcciones, i + 1)

    def comer(self, ecosistema, x, y):
        if isinstance(ecosistema.matriz[x][y], Presa):
            print(f"🍖 Depredador en ({x},{y}) se comió una presa")
            self.energia += 10
            ecosistema.matriz[x][y] = self

    def morir(self, ecosistema, x, y):
        if self.energia <= 0:
            print(f"💀 Depredador en ({x},{y}) murió de hambre")
            ecosistema.matriz[x][y] = 0


class Presa:
    def __init__(self, energia):
        self.energia = energia
        self.tipo = "Presa"

    def mover(self, ecosistema, x, y):
        print(f"🐇 Presa en ({x},{y}) intenta moverse")
        planta_x, planta_y = self.buscar_planta(ecosistema, x, y)
        if planta_x is not None and planta_y is not None:
            print(f"🌱 Presa se mueve hacia la planta en ({planta_x},{planta_y})")
            ecosistema.mover_organismo(x, y, planta_x, planta_y)
            self.comer(ecosistema, planta_x, planta_y)
        else:
            print("🚶 Presa se mueve aleatoriamente")
            self.mover_aleatorio(ecosistema, x, y)

    def buscar_planta(self, ecosistema, x, y):
        return self.buscar_planta_recursivo(ecosistema, x, y, 0, 1) or \
               self.buscar_planta_recursivo(ecosistema, x, y, 0, -1) or \
               self.buscar_planta_recursivo(ecosistema, x, y, 1, 0) or \
               self.buscar_planta_recursivo(ecosistema, x, y, -1, 0)

    def buscar_planta_recursivo(self, ecosistema, x, y, dx, dy):
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < ecosistema.n and 0 <= nuevo_y < ecosistema.n:
            if isinstance(ecosistema.matriz[nuevo_x][nuevo_y], Planta):
                return nuevo_x, nuevo_y
            return self.buscar_planta_recursivo(ecosistema, nuevo_x, nuevo_y, dx, dy)
        return None, None

    def mover_aleatorio(self, ecosistema, x, y):
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcciones)
        self.mover_aleatorio_recursivo(ecosistema, x, y, direcciones, 0)

    def mover_aleatorio_recursivo(self, ecosistema, x, y, direcciones, i):
        if i == len(direcciones):
            return

        dx, dy = direcciones[i]
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < ecosistema.n and 0 <= nuevo_y < ecosistema.n and ecosistema.matriz[nuevo_x][nuevo_y] == 0:
            ecosistema.mover_organismo(x, y, nuevo_x, nuevo_y)
            return

        self.mover_aleatorio_recursivo(ecosistema, x, y, direcciones, i + 1)

    def comer(self, ecosistema, x, y):
        if isinstance(ecosistema.matriz[x][y], Planta):
            print(f"🌿 Presa en ({x},{y}) comió una planta")
            self.energia += 3
            ecosistema.matriz[x][y] = self  # Se come la planta y ocupa su espacio

    def morir(self, ecosistema, x, y):
        if self.energia <= 0:
            print(f"💀 Presa en ({x},{y}) murió de hambre")
            ecosistema.matriz[x][y] = 0



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
        if self.ciclos >= self.ciclos_maximos or self.verificar_extincion():
            return "Simulación terminada"

        print(f"\n🔹 **Ciclo {self.ciclos + 1}:**")
        self.imprimir_matriz()
        for x in range(self.n):
            for y in range(self.n):
                organismo = self.matriz[x][y]
                if isinstance(organismo, (Depredador, Presa)):
                    organismo.mover(self, x, y)
                    organismo.comer(self, x, y)
                    organismo.energia -= 1
                    organismo.morir(self, x, y)

        self.ciclos += 1
        return self.ejecutar_ciclo()

    def verificar_extincion(self):
        return not any(isinstance(cell, (Depredador, Presa)) for row in self.matriz for cell in row)

    def imprimir_matriz(self):
        simbolos = {Depredador: "D", Presa: "P", Planta: "*", int: "."}
        for fila in self.matriz:
            print(" ".join(simbolos.get(type(celda), ".") for celda in fila))