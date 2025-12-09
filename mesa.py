
class Mesa:
    def __init__(self):
        self.vira = ""
        self.cartas = []
        self.jogadorCartas = []

    def definirVira(self, carta):
        self.vira = carta
    
    def limparMesa(self):
        self.vira = None
        self.cartas.clear()
        self.jogadorCartas.clear()
    
    def limparSubRodada(self):
        self.cartas.clear()
        self.jogadorCartas.clear()
