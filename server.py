from xmlrpc.server import SimpleXMLRPCServer
import random
import config
import os
from servico import Truco

os.system(config.CMD_CLS)


server = SimpleXMLRPCServer((config.HOST, int(config.PORT)), allow_none=True)
print(f"Servidor XML-RPC ouvindo na porta {config.PORT}...")

server.register_instance(Truco(), allow_dotted_names=True)
#server.register_instance(Truco())

try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
