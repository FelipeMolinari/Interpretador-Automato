from Automato import Automato
class Interpretador:


    def __init__(self):
        self.definicao = ""
        self.tag = ""

    def separaComando(self, cmd):
        self.tag = cmd[0:2]
        self.definicao = cmd[2:len(cmd)]

 

#Classe que recebe uma tag e uma definicão e faz a interpretação.
interp = Interpretador()
interp.separaComando("maanoq%nomeStr")
print(Interpretador.validaExpressão(interp.tag))