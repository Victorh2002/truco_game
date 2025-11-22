import xmlrpc.client
import sys
import os
import time

s = xmlrpc.client.ServerProxy('http://localhost:8000')

nome = input("Digite nome do jogador: ")
sucesso = s.criarJogador(nome)
if sucesso:
    print("Entrou com sucesso no servidor!")
else:
    print("Falha ao criar jogador no servidor.")
    sys.exit(1)

print("Aguardando o segundo jogador entrar...")

while True:
    pronto = s.jogadoresProntos()

    if pronto:
        os.system("cls")
        print("\n--- JOGO INICIADO! ---")
        break 
    else:
        print(".", end="", flush=True)
        time.sleep(2)

while True:
    print("\nSua mão atual:")
    print(s.verBaralho(nome))
    print("\n--- Menu de Ações ---")
    print("2 - Ver lista de jogadores")
    print("(Digite qualquer outra coisa para sair)")
    escolha = input("Escolha: ")

    if escolha == "2":
        print("Buscando lista de jogadores...")
        lista_de_nomes = s.listarJogadores()
        
        print("\n--- Lista de Jogadores ---")
        if not lista_de_nomes:
            print("(Nenhum jogador criado ainda)")
        else:
            for nome in lista_de_nomes:
                print(f"- {nome}")
    else:
        print("Saindo...")
        break