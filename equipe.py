class Equipe:
	def __init__(self, nome ):
		self.nome = nome
		self.listaJogadores = []
		self.pontos = 0
		self.vitoria_rodada = 0
	def addJogador( self, jogador):
		teste = [ j for j in self.listaJogadores if jogador.nome == j.nome]
		if len(teste) > 0:
			return -1
		self.listaJogadores.append(jogador)
		return 1
	def addPontos(self, pontos):
		self.pontos += pontos
