# client.py
# (Com 4 espaços!)
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

while True: # 'while 1' funciona, mas 'while True' é mais Pythonico
    print("\n--- Menu de Ações ---")
    print("1 - Criar jogador")
    print("2 - Ver lista de jogadores")
    print("3 - Gerar Maos")
    print("(Digite qualquer outra coisa para sair)")
    escolha = input("Escolha: ")

    if escolha == "1":
        nome = input("Digite nome do jogador: ")
        # Chama a função no servidor
        sucesso = s.criarJogador(nome)
        if sucesso:
            print(f"'{nome}' criado no servidor!")
        else:
            print("Falha ao criar jogador no servidor.")

    elif escolha == "2":
        print("Buscando lista de jogadores...")
        # Chama a função no servidor
        lista_de_nomes = s.listarJogadores()
        
        # Imprime o resultado que o servidor RETORNOU
        print("\n--- Lista de Jogadores ---")
        if not lista_de_nomes:
            print("(Nenhum jogador criado ainda)")
        else:
            for nome in lista_de_nomes:
                print(f"- {nome}")

    elif escolha == "3":
        print(s.gerarCartas("Victor"))
    else:
        print("Saindo...")
        break