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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM6"                  # Windows(variacao de)


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace('/dev/ttyACM0')

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        # aqui você deverá gerar os dados a serem transmitidos.
        # seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o
        # nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        # txBuffer = imagem em bytes!

        # faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

        # finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        # faça um print para avisar que a transmissão vai começar.
        # tente entender como o método send funciona!
        # Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!

        # com1.sendData(np.asarray(txBuffer))
        
        # loop para receber
        contador = 0

        while True:
            rxBuffer, nRx = com1.getData(1)
            rxSize = int.from_bytes(rxBuffer, "big")
            time.sleep(0.01)
            com1.sendData(np.asanyarray(b"\x10"))
            if rxBuffer == b"\x11":
                contador -= 1
                com1.sendData(np.asarray(contador.to_bytes(1, "big")))
                print(f"O total recebido pelo servidor foi: {contador}")
                break
            print(f"O comando({contador + 1}) enviado: {rxBuffer}")
            rxBuffer, nRx = com1.getData(rxSize)
            com1.sendData(np.asanyarray(b"\x10"))
            # time.sleep(15)
            contador += 1
            print(rxBuffer)

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        # Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        # Observe o que faz a rotina dentro do thread RX
        # print um aviso de que a recepção vai começar.

        # Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        # Veja o que faz a funcao do enlaceRX  getBufferLen

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