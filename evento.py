class Evento: #Cada envendo são dados enviados para o servidor
	def __init__(self, nome=None,  cartas=None, carta=None, truco=None, desistir=None, equipe=None, iniciar=None):
		self.nome = nome
		self.cartas = cartas
		self.carta = carta
		self.truco = truco
		self.desistir = desistir
		self.equipe = equipe
		self.iniciar = iniciar

