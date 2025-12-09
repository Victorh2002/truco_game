import xmlrpc.client
import sys
import os
import time
import config
import json
from estados import Estados
class Client:

	def __init__(self):
		self.proxy = xmlrpc.client.ServerProxy(config.SERVER)
		self.nomeUsuario = None
		self.sair = False
		self.rodada = 1
		self.cartas = []

	def menu(self):
		while self.sair != True:
			estado = self.proxy.estadoservidor()
			os.system(config.CMD_CLS)
			for e in Estados:
				if e.value == estado:
					print(f"Estado servidor:{e.name}")
			print(f"Jogador:{self.nomeUsuario}")
			print("----------------------------")
			match estado:
				case Estados.INICIOJOGO.value:
					self.menu_estado_inicio_jogo()
				case Estados.EMBARALHAMENTO.value:
					print("Estado embaralhamento")
				case Estados.DISTRIBUICAO.value:
					self.menu_distribuicao()
				case Estados.LANCE.value:
					#print("Estado lance")
					self.menu_lance()
				case Estados.TRUCO.value:
					print("Estado truco")
				case Estados.VITORIAEQUIPE:
					self.menuVitoria()
				case _:
					print("Estado desconhecido")

	def menuVitoria(self):
		strVE = self.proxy.vitoriaEquipe()
		objVe = json.loads(strVE)
		os.system(config.CMD_CLS)
		print("Equipe vendora: ", objVE["equipe"])
		print("Pontuação: ", objVE["pontos"])
		resposta=input("Digite '1' para iniciar nova partida")
		if resposta == '1':
			self.proxy.restart()



	def menu_estado_inicio_jogo(self):
		print("Inicio de jogo:")
		print("Selecione uma opção:")
		lstMenu = []
		if self.nomeUsuario == "" or self.nomeUsuario == None:
			lstMenu.append("Cadastrar jogador")
		lstMenu.append("Listar jogadores")
		lstMenu.append("Listar pontuação")
		lstMenu.append("Solicitar inicio de jogo")
		lstMenu.append("Sair")
		x = 1
		for opcao in lstMenu:
			print(f"{x:2d} - {opcao}")  
			x += 1

		res = input("Opção: ")
		if res in ['1', '2', '3', '4' , '5']:
			resposta = int(res)
		else:
			resposta = -1
		
		if resposta == -1:
			print("Opção desconhecida")
			input("Tecle 'ENTER' para continuar")
		elif  lstMenu[resposta-1]  ==  "Cadastrar jogador" :
			os.system(config.CMD_CLS)
			print("Adição de usuário")
			nome = input("nome:")
			self.nomeUsuario = nome
			equipe = input("equipe (vazio sozinho):")
			res = self.proxy.addJogador(nome, equipe)
			resposta = json.loads(res)
			print(resposta['mensagem'])
			input("Tecle 'ENTER' para continuar")
		elif  lstMenu[resposta-1]  ==  "Listar jogadores" :
			print(self.proxy.mostrarJogo())
			input("\n\nAperte 'ENTER' para continuar")
		elif  lstMenu[resposta-1]  ==  "Listar pontuação" :
			print(self.proxy.MostrarPontuacao())
			input("\n\nAperte 'ENTER' para continuar")
		elif  lstMenu[resposta-1]  ==  "Solicitar inicio de jogo" :
			print("Solicitando inicio de jogo")
			resposta = self.proxy.iniciar()
			print(f"{resposta}")
			input("\n\nAperte 'ENTER' para continuar")
		elif  lstMenu[resposta-1]  ==  "Sair" :
			self.sair=True
		else:
			print("Opção desconhecida")
			input("Tecle 'ENTER' para continuar")
	def menu_distribuicao(self):
		if len(self.cartas) >  0 :
			print("Aguarde outros usuários pegarem as cartas")
			input("Aperte 'ENTER' para continuar")
			return
		print("1 - Solicitar cartas")
		print("2 - Sair")
		resposta = input("opção:")
		match resposta:
			case "1":
				print(self.nomeUsuario)
				strJson= self.proxy.solicitarCartas( self.nomeUsuario)
				if len(strJson) > 1:
					cartas= json.loads(strJson)
					self.cartas= cartas
					self.rodada = 1
				else:
					print(f"O usuário {self.nomeUsuario} já pegou cartas")
				print(self.cartas)
				input("Aperte 'ENTER' para continuar")
			case '2':
				self.sair= True
			case _ :
				print("Opção desconhecida")


	def menu_lance(self):
		if self.proxy.estadoservidor() != Estados.LANCE.value:
			return
		rodada_servidor = self.proxy.obterRododa()
		print(f"Rodada no servidor {rodada_servidor}")
		print(f"Rodada no cliente {self.rodada}")
		print("----------------------------")
		print("Estado de fazer lance")
		print("1 - Desistir")
		print("2 - Listar Mesa")
		contar = 0
		if self.rodada == rodada_servidor:
			for carta in self.cartas:
				print(f"{contar + 3} - Jogar carta  {carta}") 
				contar = contar + 1
		resposta = input("Opção:")
		match resposta:
			case '1':
				self.proxy.lanceCarta(self.nomeUsuario, '{"desistir":"SIM", "jogador":"' + self.nomeUsuario + '"}')
			case '2':
				os.system(config.CMD_CLS)
				print(self.proxy.MostrasCartasNaMesa())
				input("Tecle 'ENTER' para continuar")
			case '3':
				if len(self.cartas) < 1 or self.rodada != rodada_servidor:
					print("Opção desconhecida")
					input("Tecle 'ENTER' para continuar")
				else:
					teste = self.proxy.lanceCarta( self.nomeUsuario,  json.dumps(self.cartas[0]));
					if teste:
						self.cartas.remove(self.cartas[0])
						self.rodada = rodada_servidor + 1
			case '4':
				if len(self.cartas) < 2 or self.rodada != rodada_servidor:
					print("Opção desconhecida")
					input("Tecle 'ENTER' para continuar")
				else:
					teste = self.proxy.lanceCarta( self.nomeUsuario,  json.dumps(self.cartas[1]));
					if teste:
						self.cartas.remove(self.cartas[1])
						self.rodada = rodada_servidor + 1
			case '5':
				if len(self.cartas) < 3 or self.rodada != rodada_servidor:
					print("Opção desconhecida")
					input("Tecle 'ENTER' para continuar")
				else:
					teste = self.proxy.lanceCarta( self.nomeUsuario,  json.dumps(self.cartas[2]));
					if teste:
						self.cartas.remove(self.cartas[2])
						self.rodada = rodada_servidor + 1
			case _:
				print("Opção desconhecida")
				input("Tecle 'ENTER' para continuar")

if __name__ == '__main__':
	cliente = Client()
	cliente.menu()
