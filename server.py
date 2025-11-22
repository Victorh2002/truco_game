from xmlrpc.server import SimpleXMLRPCServer
import random

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []
        self.pontos = 0

class Baralho:
    def __init__(self):
        self.valores = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        self.naipes = ["Ouros", "Espadas", "Copas", "Paus"]
        self.baralho = []

    def criarBaralho(self):
        for naipe in self.naipes:
            for valor in self.valores:
                self.baralho.append(f"{valor} de {naipe}")

    def embaralharBaralho(self):
        random.shuffle(self.baralho)

jogadores = []

baralho = Baralho()

baralho.criarBaralho()
baralho.embaralharBaralho()

def distribuirCartas():
    mao1 = []
    for _ in range(3):
        mao1.append(baralho.baralho.pop(0))
    jogadores[0].mao = mao1
    
    mao2 = []
    for _ in range(3):
        mao2.append(baralho.baralho.pop(0))
    jogadores[1].mao = mao2

def criarJogador(nome):
    if len(jogadores) == 2:
        print("Erro ao criar jogador: Servidor Lotado!")
        return False
     
    try:
        jogadores.append(Jogador(nome))
        print(f"Jogador '{nome}' criado com sucesso.")
        return True 
    except Exception as e:
        print(f"Erro ao criar jogador: {e}")
        return False 

def listarJogadores():
    nomes_dos_jogadores = []
    for jogador in jogadores:
        nomes_dos_jogadores.append(jogador.nome)
    
    print(f"Enviando lista de jogadores: {nomes_dos_jogadores}")
    return nomes_dos_jogadores 

def verBaralho(nome):
    for jogador in jogadores:
        if jogador.nome == nome:
            return jogador.mao

jogo_iniciado = False

def jogadoresProntos():
    if len(jogadores) == 2:
        distribuirCartas()
        return True
    return False

def iniciarJogo():
    teste = 1

server = SimpleXMLRPCServer(('localhost', 8000))
print("Servidor XML-RPC ouvindo na porta 8000...")

server.register_function(criarJogador)
server.register_function(listarJogadores)
server.register_function(verBaralho)
server.register_function(jogadoresProntos)
server.register_function(iniciarJogo)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')