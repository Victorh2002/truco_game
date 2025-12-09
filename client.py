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
					print(f"Estado {e.name}")
			print(f"Jogador:{self.nomeUsuario}")
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
				case _:
					print("Estado desconhecido")


	def menu_estado_inicio_jogo(self):
		print("Inicio de jogo:")
		print("Selecione uma opção:")
		print("1 - Cadastrar jogador.")
		print("2 - Listar jogadores")
		print("3 - Listar pontuação")
		print("4 - Iniciar")
		print("5 - Sair")
		resposta = input("Opção: ")
		match resposta:
			case '1':
				nome = input("nome:")
				self.nomeUsuario = nome
				equipe = input("equipe (vazio sozinho):")
				print(f"equipe{type(equipe)} nome {type(nome)}")
				resposta = self.proxy.addJogador(nome, equipe)
				if resposta:
					print(f"Gerou usuário {nome}")
				else:
					print(f"Erro ao gerar o usuário {nome}")
			case '2':
				print(self.proxy.mostrarJogo())
				input("\n\nAperte 'ENTER' para continuar")
			case '3':
				print(self.proxy.MostrarPontuacao())
				input("\n\nAperte 'ENTER' para continuar")
			case '4':
				print("Solicitando inicio de jogo")
				self.proxy.iniciar()
			case '5':
				self.sair=True
			case _:
				print("Opção desconhecida")
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
		print("Estado de fazer lance")
		print("1 - Desistir")
		print("2 - Listar Mesa")
		contar = 0
		rodada_servidor = self.proxy.obterRododa()
		print(f"rodada_servidor {rodada_servidor}")
		print(f"self.rodada {self.rodada}")
		if self.rodada == rodada_servidor:
			for carta in self.cartas:
				print(f"{contar + 3} - Jogar carta  {carta}") 
				contar = contar + 1
		resposta = input("Opção:")
		match resposta:
			case '1':
				self.proxy.lanceCarta(self.nomeUsuario, '{"desistir":"SIM", "jogador":"' + 'self.nomeUsuario"}')
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
