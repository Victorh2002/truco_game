



jogadores = []
placarSubRodada = []
vencedorSubRodada = None
mesa = Mesa()
baralho = Baralho()
vezJogador = None
vezJogadorRodada = None

baralho.criarBaralho()
baralho.embaralharBaralho()
iniciarRodadaLock = False

def definirVencedor():
    i = 0
    maiorCarta = None
    indexVencedor = -1
    for carta in mesa.cartas:
        if maiorCarta == None:
            maiorCarta = carta
            indexVencedor = i
        else:
            splitMaiorCarta = maiorCarta.split(" de ")
            splitCartaAtual = carta.split(" de ")

            valorCartaAtual = splitCartaAtual[0]
            naipeCartaAtual = splitCartaAtual[1]

            valorMaiorCarta = splitMaiorCarta[0]
            naipeMaiorCarta = splitMaiorCarta[1]

            indexValorCartaAtual = baralho.valores.index(valorCartaAtual)
            indexValorMaiorAtual = baralho.valores.index(valorMaiorCarta)

            if indexValorCartaAtual > indexValorMaiorAtual:
                maiorCarta = carta
                indexVencedor = i
            elif indexValorCartaAtual == indexValorMaiorAtual:
                return "Empache"
            
        i = i + 1
    
    nomeVencedor = mesa.jogadorCartas[indexVencedor]
    return nomeVencedor

def distribuirCartas():
    mao1 = []
    for _ in range(3):
        mao1.append(baralho.baralho.pop(0))
    jogadores[0].mao = mao1

    mao2 = []
    for _ in range(3):
        mao2.append(baralho.baralho.pop(0))
    jogadores[1].mao = mao2

    mesa.definirVira(baralho.baralho.pop(0))

def criarJogador(nome):
    if len(jogadores) == 2:
        print("Erro ao criar jogador: Servidor Lotado!")
        return False
    
    if len(jogadores) > 0:
        if nome == jogadores[0].nome:
            print("Erro ao criar jogador: Jogador 0 tem o mesmo nome!")
            return False
     
    try:
        jogadores.append(Jogador(nome))
        print(f"Jogador '{nome}' criado com sucesso.")
        return True 
    except Exception as e:
        print(f"Erro ao criar jogador: {e}")
        return False 

def listarJogadores():
    nomes_dos_jogadores = []
    for jogador in jogadores:
        nomes_dos_jogadores.append(jogador.nome)
    
    print(f"Enviando lista de jogadores: {nomes_dos_jogadores}")
    return nomes_dos_jogadores 

def verBaralho():
    return baralho.baralho

def verMao(nome):
    for jogador in jogadores:
        if jogador.nome == nome:
            return jogador.mao

def verPlacarSubRodada():
    return placarSubRodada

def verMesa():
    return [mesa.cartas, mesa.vira]

jogo_iniciado = False

def jogadoresProntos():
    if len(jogadores) == 2:
        return True
    return False

def iniciarRodada():
    global iniciarRodadaLock, placarSubRodada, vezJogadorRodada, vezJogador, vencedorSubRodada
    if iniciarRodadaLock:
        return False
    iniciarRodadaLock = True

    for jogador in jogadores:
        jogador.limparJogador()

    if vezJogadorRodada == None or vezJogadorRodada == jogadores[1].nome:
        vezJogadorRodada = jogadores[0].nome
    else:
        vezJogadorRodada = jogadores[1].nome

    vezJogador = vezJogadorRodada
    placarSubRodada = []
    vencedorSubRodada = None
    mesa.limparMesa()

    baralho.limparBaralho()
    baralho.criarBaralho()
    baralho.embaralharBaralho()
    
    try:
        return distribuirCartas()
    finally:
        iniciarRodadaLock = False
        return True
    
def tacarCarta(indexCarta, nomeJogador):
    global vezJogador, vencedorSubRodada
    for jogador in jogadores:
        if jogador.nome == nomeJogador:
            carta = jogador.mao.pop(indexCarta)
            mesa.cartas.append(carta)
            mesa.jogadorCartas.append(nomeJogador)
            break

    if len(mesa.cartas) == 1:
        for jogador in jogadores:
            if jogador.nome != nomeJogador:
                vezJogador = jogador.nome
                break
    
    elif len(mesa.cartas) == 2:
        vencedor = definirVencedor()
        if vencedor == "Empache":
            print("Empache!")
            placarSubRodada.append("Empache")
            vencedorSubRodada = "Empache"
            vezJogador = mesa.jogadorCartas[0]
            mesa.limparSubRodada()
        else:
            print(f"Vencedor: {vencedor}")
            vezJogador = vencedor
            placarSubRodada.append(vencedor)
            vencedorSubRodada = vencedor
            mesa.limparSubRodada()

    return True

def obterVencedorSubRodada():
    if vencedorSubRodada == None:
        return False
    return vencedorSubRodada

def obterVezJogador():
    if len(jogadores[0].mao) == 0 and len(jogadores[1].mao) == 0:
        print(len(jogadores[0].mao), len(jogadores[1].mao))
        return False
    return vezJogador
