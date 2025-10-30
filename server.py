from xmlrpc.server import SimpleXMLRPCServer
import random

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []
        self.pontos = 0

# O estado do jogo (a lista de jogadores)
jogadores = []

# --- Funções que o servidor vai expor ---

def criarJogador(nome):
    """
    Cria um novo jogador e o adiciona à lista.
    Retorna True se foi sucesso.
    """
    try:
        jogadores.append(Jogador(nome))
        print(f"Jogador '{nome}' criado com sucesso.")
        return True # Retorna "sucesso" para o cliente
    except Exception as e:
        print(f"Erro ao criar jogador: {e}")
        return False # Retorna "falha" para o cliente

def listarJogadores():
    """
    Retorna uma LISTA DE STRINGS com os nomes dos jogadores.
    """
    # Nós não podemos retornar 'jogadores' (que é uma lista de OBJETOS)
    # Então, criamos uma nova lista apenas com os NOMES.
    nomes_dos_jogadores = []
    for j in jogadores:
        nomes_dos_jogadores.append(j.nome)
    
    print(f"Enviando lista de jogadores: {nomes_dos_jogadores}")
    return nomes_dos_jogadores # Retorna a lista de NOMES para o cliente

def gerarCartas(nome):
    for j in jogadores:
        for index in range(3):
            j.mao.append(random.randint(1, 10))
    return jogadores

# --- Configuração do Servidor ---

# Cria o servidor
server = SimpleXMLRPCServer(('localhost', 8000))
print("Servidor XML-RPC ouvindo na porta 8000...")

# Registra as FUNÇÕES (e não instâncias)
server.register_function(criarJogador)
server.register_function(listarJogadores)
server.register_function(gerarCartas)

# Roda o servidor
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')