from servico import Truco
import json
t = Truco()
t.addJogador("Valdeir","")
t.addJogador("Luiz","Prestes")
t.addJogador("Vagner", "Prestes")

print("\n\n",t.mostrarJogo())

t.iniciar()

t.solicitarCartas("Valdeir")
t.solicitarCartas("Luiz")
t.solicitarCartas("Vagner")




print(f"Estado {t.estado}")
