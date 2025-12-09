from estados import Estados 
from equipe import Equipe
from jogador import Jogador
from baralho import Baralho
import json
import random

class Truco:
	def __init__(self):
		self.estado = Estados.INICIOJOGO
		self.listaEquipe = []
		self.listaRodadas= {1:[], 2:[] , 3:[]}
		self.rodada = 1
		self.baralho = []
		self.registraJogadorCarta = []
		self.pontos_rodada = 1
		self.pontos_truco = 0
		self.equipe_truco =''

	
	def estadoservidor(self):
		return self.estado.value

	
	def verificaUsuario(self, nomeUsuario):
		return nomeUsuario in self.registraJogadorCarta

	
	def iniciar(self):
		if len(self.listaEquipe) < 2:
			strRetorno = "precisa de pelo menos dois jogadores com equipes diferentes para iniciar o jogo"
			print(strRetorno)
			return strRetorno
		self.estado = Estados.EMBARALHAMENTO
		t = Baralho()
		self.baralho = t.criarBaralho()
		self.rodada=1
		self.estado = Estados.DISTRIBUICAO
		self.listaJogadorDistribuicao = []
		self.listaJogadorLances = []
		strRetorno = "Iniciar o estado Distribuição de cartas"
		return strRetorno
	def proximaRodada(self):
		self.estado = Estados.INICIOJOGO
		self.rodada = 1
		self.registraJogadorCarta = []
		self.pontos_rodada = 1
		self.pontos_truco = 0
		self.equipe_truco =''

	

	def solicitarCartas(self, nomeUsuario):
		if self.verificaUsuario(nomeUsuario):
			print("Nome já cadastrado")
			return ""
		elif  self.estado != Estados.DISTRIBUICAO:
			print("Servidor não esta em estado de distribuição de cartas")
			return ""
		else:
			self.registraJogadorCarta.append(nomeUsuario)
			listaTeste=[]
			testeFimDistribuicao = True
			if not nomeUsuario in self.listaJogadorDistribuicao:
				self.listaJogadorDistribuicao.append(nomeUsuario)
			numjogadores = 0
			for equipe in self.listaEquipe:
				for u in equipe.listaJogadores:
					numjogadores = numjogadores + 1
					print(f"{u.nome} -> {self.listaJogadorDistribuicao}")
					if not u.nome in self.listaJogadorDistribuicao:
						testeFimDistribuicao = False
			if testeFimDistribuicao == True and numjogadores > 1:
				self.estado = Estados.LANCE
			cont = 1
			cartas = []
			while cont <=3:
				random.shuffle(self.baralho)
				cartas.append(self.baralho.pop())
				cont = cont + 1
			print(f"--->cartas{cartas}")
			return json.dumps( cartas ) 

	

	def addJogador(self, nome, nome_equipe):
		if len(nome) < 1:
			print("Nome inválido")
			return -1
		if len(nome_equipe) < 1 :
			equipe = nome
		else:
				equipe = nome_equipe
		jogador = Jogador(nome, equipe)
		if self.estado != Estados.INICIOJOGO:
			print("Erro: não pode jogador neste momento porque o jogo já começou")
			return 0
		print(f"Adicionado {nome}", end="\n")
		if len(equipe) > 0 :
			print(f"Procurando equipe {equipe}...")
			equipe_lista = [ e for e in self.listaEquipe if e.nome == nome_equipe]
			if len(equipe_lista) > 0:
				e = equipe_lista[0]
				print(f"Achou equipe {e.nome}")
			else:
				print(f"Nao localizou, gerando equipe {equipe}...")
				e = Equipe(equipe)
				self.listaEquipe.append(e)
			e.addJogador(jogador)
		else:
			print("")
		return 1
	

	def mostrarJogo(self):
		strEquipes = ""
		for equipe in self.listaEquipe:
			strEquipe2 =""
			for jogador in equipe.listaJogadores:
				strEquipe2 +=f"'{jogador.nome}',"
			strEquipe2 = strEquipe2[:-1]
			strEquipes +="{ 'equipe':'" + equipe.nome + "', 'jogadores':[" + strEquipe2 + "]},"
		strEquipes= strEquipes[:-1]
		strEquipes = "{" + strEquipes + "}"
		return strEquipes
	def _verificaJogador(self, nomeJogador):
		for equipe in self.listaEquipe:
			for jogador in equipe.listaJogadores:
				if jogador.nome == nomeJogador:
					return True
		return False
	def _verificaJogadaJogador(self, nomeJogador):
		if len(self.listaRodadas[self.rodada ]) < 1:
			return False
		print(f"lance\n\n{self.listaRodadas[self.rodada]}\n\n")
		for jogada in self.listaRodadas[self.rodada]:
			if jogada["jogador"] == nomeJogador:
				return True
		return False



	def fimRodada(self):
		for equipe in self.listaEquipe:
			for jogador in equipe.listaJogadores:
				if self._verificaJogadaJogador(jogador.nome) == False:
					return False
		return True



	def _localizaEquipe(self, nomeJogador):
		for equipe in self.listaEquipe:
			for jogador in equipe.listaJogadores:
				print(f"jogador {jogador.nome} nomeJogador {nomeJogador}")
				if jogador.nome == nomeJogador:
					return equipe
		return None



	def _verificaVitoriaRodada(self, r):
		lista = []
		baralho = Baralho()
		for carta in self.listaRodadas[r]:
			print(f'carta {carta}')
			minhacarta = {'jogador':carta['jogador'], 'peso': baralho.valor(carta['carta']['simbolo'], carta['carta']['naipe'])}
			lista.append(minhacarta)
		lista_ordenada = sorted( lista, key=lambda p: p['peso'])
		vencedor = lista_ordenada[-1:]
		if len(vencedor) != 1:
			return ""
		
		equipe = self._localizaEquipe(vencedor[0]["jogador"])
		if equipe != None:
			print(f"equipe {equipe}")
			equipe.vitoria_rodada += 1
			print(equipe)
			if equipe.vitoria_rodada == 3:
				equipe.pontos += self.pontos_rodada
				self.proximaRodada()
			return vencedor
		else:
			print("Error, o jogador não pertence a uma equipe")
			return ""




	def obterEquipe(self, nomeJogador):
		equipe = None
		for e in self.listaEquipe:
			for jogador in e.listaJogadores:
				if jogador.nome == nomeJogador:
					return e
		return None
			


	def obterTruco(self):
		return json.dumps({"equipe":self.equipe_truco , "pontos_truco":self.pontos_truco})

	def _addVitoriaEquipeJogador(self, nomeJogador):
		equipe = self.obterEquipe(nomeJogador)
		if equipe != None:
			for e in self.listaEquipe:
				if e != equipe:
					e.vitoria_rodada += 1


	def lanceCarta(self, jogador, carta):
		carta_obj = json.loads(carta)
		if self._verificaJogadaJogador(jogador) == False:
			self.listaRodadas[self.rodada].append({"jogador":jogador, "carta":carta_obj})
			if 'desisitir' in carta_obj and 'jogador' in carta_obj:
				equipe = self.obterEquipe(carta_obj['jogador'])
				if equipe != None:
					for e in self.listaEquipe:
						if e != equipe:
							e.pontos += 1
				self.proximaRodada()
				return True
			if 'truco' in carta_obj and 'jogador' in carta_obj:
				self._addVitoriaEquipeJogador(carta_obj['jogador'])
				return True
			if 'aceito_truco' in carta_obj and 'jogador' in carta_obj:
				equipe = self.obterEquipe(carta_obj['jogador'])
				if equipe == None:
					return False
				if equipe.nome == self.equipe_truco:
					return False
				self.pontos_rodada = self.pontos_truco
				self.pontos_truco = 0
				self.equipe_truco = ""
				self.estado = Estados.LANCE
				return True
			elif self.fimRodada():
				print("Fim de rodada")
				vitorioso = self._verificaVitoriaRodada(self.rodada)
				print(f"vitorioso{vitorioso}")
				self._addVitoriaEquipeJogador(vitorioso[0]['jogador'])
				self.rodada += 1
				if self.rodada > 3:
					self.rodada = 1
					self.estado = Estados.INICIOJOGO
					sorted(self.listaEquipe, key=lambda e : e.vitoria_rodada, reverse=True)
					self.listaEquipe[0].pontos += self.pontos_rodada
					for e in self.listaEquipe:
						e.vitoria_rodada = 0
			return True
		return False



	def obterRododa(self):
		return self.rodada
		
		



	def MostrasCartasNaMesa(self):
		print(self.listaRodadas[self.rodada])
		return json.dumps(self.listaRodadas[self.rodada])

	def MostrarPontuacao(self):
		lst = []
		for equipe in self.listaEquipe:
			lst.append({"nome":equipe.nome, "pontos":equipe.pontos})
		sorted(lst, key=lambda e:e['pontos'])
		print(f"lst {lst}")
		return json.dumps(lst)


	def listarCartas(self):
		for lance in self.listaRodadas[self.rodada]:
			print(f"jogador:{lance['jogador']} carta:{lance['carta']}")


