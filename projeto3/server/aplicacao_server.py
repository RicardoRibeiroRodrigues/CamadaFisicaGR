#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import time
import numpy as np
from datagrama import monta_header
from utils import bytes_to_list

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM6"                  # Windows(variacao de)

HANDSHAKE = 0
RESPOSTA_HANDSHAKE = b"\x01"
DADOS = 2
COMANDOS = b"\x03"
CONFIRMACAO = b"\x04"
ERRO = b"\x05"
IPV4 = b"\x01"
IPV6 = b"\x02"
PC_RICARDO = b"\x01"
PC_FONTANA = b"\x02"
EOP = b"\xFF\xFF\xFF\xFF"


def resposta(com1, head, resposta, n_pacote=0):

    n_pacote = n_pacote.to_bytes(1, byteorder='big')
    header = monta_header(
        resposta,
        IPV6,
        n_pacote,
        b"\x01",
        PC_RICARDO,
        PC_FONTANA,
        b"\x01",
        b"\x00\x00\x00",
    )
    pacote = (header+b"\x00"+EOP)
    com1.sendData(np.asarray(pacote))
    time.sleep(0.01)
"""     com1.sendData(np.asarray(b"\x00"))
    time.sleep(0.01)
    com1.sendData(np.asarray(EOP))
    time.sleep(0.01) """


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace('/dev/ttyACM0')

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        while True:
            content = b""
            rxBufferHeader, nRx = com1.getData(10)
            if rxBufferHeader[0] == HANDSHAKE:
                size = rxBufferHeader[3]
                info, _ = com1.getData(size)
                final, _ = com1.getData(4)
                resposta(com1, rxBufferHeader, RESPOSTA_HANDSHAKE)
            if rxBufferHeader[0] == DADOS:
                message_size = rxBufferHeader[6]
                i = 0
                while i < message_size:
                    try:
                        if i != 0:
                            rxBufferHeader, nRx = com1.getData(10)
                        size = rxBufferHeader[3]
                        info, _ = com1.getData(size)
                        time.sleep(0.05)
                        final, _ = com1.getData(4)
                        pacote_certo = rxBufferHeader[2] == i
                        if not pacote_certo:
                            print("O número do pacote está incorreto, reenviando número do pacote correto!")
                        print("info: {}" .format(info))
                        print("i: {}".format(i))
                        if bytes_to_list(final) == bytes_to_list(EOP) and pacote_certo:
                            content += info
                            i += 1
                            resposta(com1, rxBufferHeader, CONFIRMACAO)
                            print("uma resposta recebida")
                        else:
                            print("deu errado, to no else")
                            if com1.rx.getBufferLen() > 0:
                                print("Tamanho informado errado")
                            com1.rx.clearBuffer()
                            resposta(com1, rxBufferHeader, ERRO, i)
                    except TimeoutError:
                        print("Tempo excedido! Tentar novamente.")
                        resposta(com1, rxBufferHeader, ERRO, i)
                with open("img/icon.png", "wb") as img:
                    img.write(content)
                print("Receba!!!! Graças a deus, SIUUUUU!!!")
                break
                        


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
