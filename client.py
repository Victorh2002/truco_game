import xmlrpc.client
import sys
import os
import time

s = xmlrpc.client.ServerProxy('http://127.0.0.1:8000')

os.system("cls")

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
    s.iniciarRodada()
    while True:
        vezJogador = s.obterVezJogador()
        if vezJogador == False:
            break
        
        os.system("cls")
        mesa = s.verMesa()
        vencedor = s.obterVencedorSubRodada()
        placarSubRodada = s.verPlacarSubRodada()
        if vencedor == "Empache":
            print("\nEmpache!")
        elif vencedor:
            print(f"\nTorna: {vencedor}")
        print(f"\nPlacar Atual Sub Rodada: {placarSubRodada}")
        print("\nSua mão atual:")
        print(s.verMao(nome))
        print("\nVira:")
        print(mesa[1])
        print("\nMesa atual:")
        print(mesa[0])

        if vezJogador == nome:
            print("\n--- SUA VEZ ---")
            print("\n--- Menu de Ações ---")
            print("1 - Ver Baralho")
            print("2 - Ver lista de jogadores")
            print("3 - Tacar Carta")
            print("(Digite qualquer outra coisa para sair)")
            escolha = input("Escolha: ")
            
            if escolha == "1":
                baralho = s.verBaralho()
                print(f"\nQuantidade de cartas no baralho:{len(baralho)}")
                print(baralho)

            elif escolha == "2":
                print("Buscando lista de jogadores...")
                lista_de_nomes = s.listarJogadores()
                
                print("\n--- Lista de Jogadores ---")
                if not lista_de_nomes:
                    print("(Nenhum jogador criado ainda)")
                else:
                    for nome in lista_de_nomes:
                        print(f"- {nome}")

            elif escolha == "3":
                print("\nDigite o índice da carta que deseja tacar")
                indexCarta = input("Escolha: ")
                indexCarta = int(indexCarta)
                s.tacarCarta(indexCarta - 1, nome)
                os.system("cls")

            else:
                print("Saindo...")
                break
        
        elif vezJogador != nome: 
            print("\n--- Vez do adversário aguarde ---")
            time.sleep(2)