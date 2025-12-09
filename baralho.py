class Baralho:
	def __init__(self):
		self.valores = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
		self.naipes = ["Ouros", "Espadas", "Copas", "Paus"]
		self.pontos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.baralho = self.criarBaralho()

	def criarBaralho(self):
		baralho = []
		for naipe in self.naipes:
			for valor in self.valores:
				baralho.append({'simbolo':valor, 'naipe':naipe, 'texto': valor + " de " + naipe})
		return baralho

	def embaralharBaralho(self):
		random.shuffle(self.baralho)

	def limparBaralho(self):
		self.baralho.clear()
	def valor(self, strSimbolo, strNaipe):
		if not strSimbolo in self.valores:
			return -1
		if not strNaipe in self.naipes:
			return -1
		return (self.valores.index(strSimbolo)+ 1) * ((self.naipes.index(strNaipe)+1) * 10)
