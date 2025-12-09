
class Jogador:
	def __init__(self, nome, equipe):
		self.nome = nome
		self.equipe = equipe
		self.mao = []

	def limparJogador(self):
		self.mao = []
