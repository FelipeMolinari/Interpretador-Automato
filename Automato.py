# Trabalho de FTC
# Montar um programa capaz de montar um automato através da expressão regular em sua forma "polonesa", Automato
# deve conseguir identificar se a palavra está contida no alfabeto.
# Felipe Cardoso Lima Molinari
# v2. 02/11

import math
import copy

class Automato:

    LAMBDACONSTANTE = "lambda"

    def __init__(self, estadoIni , estadosFim, funcTransf, alfabeto):
        self.estadoIni = estadoIni
        self.estadosFim = estadosFim
        self.funcTransf = funcTransf
        self.estadoAtual = estadoIni
        self.alfabeto = alfabeto
    
    
    def verificaPalavra(self, palavra):
        palavraValida = self.validaPalavra(palavra)
        if palavraValida:
            for letra in palavra:
                self.estadoAtual = self.funcTransf[self.estadoAtual][letra][0]
            if(Automato.LAMBDACONSTANTE in self.funcTransf[self.estadoAtual]):
                self.estadoAtual = self.funcTransf[self.estadoAtual][letra]
                print("palavra contida no alfabeto")
            elif self.estadoAtual in self.estadosFim :
                print("palavra contida no alfabeto")
            else:
                print("palavra ñ contida no alfabeto")

        else:
            print("palavra inválida")



# Dividir para conquistar (Ainda em produção) 
    # def verificaPalavraRecursiva(self, palavra,funcTransf, estado, simbolo):

    #     if(len(palavra) == simbolo):
    #         if(estado in self.estadosFim):
    #             return True
    #         else: return False

    #     if(int(len(funcTransf[estado][palavra[simbolo]])/2)>=1):
    #         divQtdSimbolos = (int((len(funcTransf[estado][palavra[simbolo]])/2)+0.5))
    #         div1 = funcTransf[estado][palavra[simbolo]][0:divQtdSimbolos]
    #         div2 = funcTransf[estado][palavra[simbolo]][divQtdSimbolos:divQtdSimbolos*2]

    #         #não quero passar por referência
    #         funcTransf1 = copy.deepcopy(funcTransf)
    #         del funcTransf1[estado][palavra[simbolo]]
    #         funcTransf1[estado][palavra[simbolo]] = div1

    #         #não quero passar por referência
    #         funcTransf2 = copy.deepcopy(funcTransf)
    #         del funcTransf2[estado][palavra[simbolo]]
    #         funcTransf2[estado][palavra[simbolo]] = div2
    #         input("Entrou no primeiro")
    #         ramo1 = self.verificaPalavraRecursiva(palavra, funcTransf1, estado, simbolo)
    #         ramo2 = self.verificaPalavraRecursiva(palavra, funcTransf2, estado, simbolo)
    #         return ramo1 or ramo2
    #     else: 
    #         novoEstado = funcTransf[estado][palavra[simbolo]] 
    #         print(novoEstado)
    #         input("Entrou no segundo")
    #         return self.verificaPalavraRecursiva(palavra, funcTransf, novoEstado, simbolo+1)

    
    def validaPalavra(self, palavra):
            for letra in palavra:
                if letra not in self.alfabeto:
                    return False
            return True

    #Gera um automato que aceita apenas um simbolo
    @staticmethod
    def geraAutomatoComUmSimbolo(simbolo):
        trans_func_novo = {'q1' : {'{}'.format(simbolo) : ['q2']}, 'q2':{Automato.LAMBDACONSTANTE: 'q3'}, 'q3':{}}
        novoAutomato = Automato("q1", ["q3"], trans_func_novo, '{}'.format(simbolo))
        return novoAutomato
    


    def unirAlfabetos(self,automato2):
        alfabeto1 = self.alfabeto
        alfabeto2 = automato2.alfabeto
        
        for x in alfabeto2:
            alfabeto1.append(x)
        return set(alfabeto1)

    def alteraNomeEstados(self,numEstados):

        # Inverte a função de transferencia, é necessário fazer isso para que não ocorra conflito entre os elementos iniciais com os próximos
        # visto sempre os estados originais terão valor menor que o novo estado. Ex: q1 passa a ser q2, podendo conflitar com o q2 original. 
        auxEstados = list(self.funcTransf)[::-1]

        
        for estado in auxEstados:
            auxTransicoes = list(self.funcTransf[estado])
            for transicoes in auxTransicoes:
                
                # Pode possuir mais transições para o mesmo valor
                for estadoTransicao in range(len(self.funcTransf[estado][transicoes])):
                    novoEstadoTransicao = int(self.funcTransf[estado][transicoes][estadoTransicao][1])+numEstados
                    self.funcTransf[estado][transicoes][estadoTransicao] = 'q{}'.format(novoEstadoTransicao)

            novoEstado = int(estado[1])+numEstados

            funcAux = self.funcTransf.pop(estado)

            self.funcTransf['q{}'.format(novoEstado)] = funcAux
        self.estadoIni = '{}'.format(int(self.estadoIni[1]) + numEstados)

        for x in range(len(self.estadosFim)):
            self.estadosFim[x] = 'q{}'.format(int(self.estadosFim[x][1]) + numEstados)

        inicial = {Automato.LAMBDACONSTANTE:"q{}".format(numEstados+1)}
        self.funcTransf["q1"] = inicial


    def criaNovoEstadoComTransicoesLambdas(self, novoFinal):
        for estado in self.funcTransf:

            if estado in self.estadosFim:
                self.funcTransf[estado][Automato.LAMBDACONSTANTE] = 'q{}'.format(novoFinal)
        
       

    def getQuantidadeDeEstados(self, aut2):
        return len(self.funcTransf) + len(aut2.funcTransf)

    def unirAutomatos(self, vaiUnir):
        self.alteraNomeEstados(1)

        numEstadosSelfAutomato = len(self.funcTransf)
        quantidadeTotalEstados = len(self.funcTransf) + len(vaiUnir.funcTransf)

        #primeiro estado deve possuir q{valor} mair oque o ultimo q{valor} do automato self
        vaiUnir.alteraNomeEstados(numEstadosSelfAutomato)
        

        self.criaNovoEstadoComTransicoesLambdas(quantidadeTotalEstados+1)
        vaiUnir.criaNovoEstadoComTransicoesLambdas(quantidadeTotalEstados+1)

        # estado inicial q1 deve possuir trasição lambda para ambos os automatos
        estadoInicialAux = []
        estadoInicialAux.append(self.funcTransf["q1"].pop(Automato.LAMBDACONSTANTE))
        estadoInicialAux.append(vaiUnir.funcTransf["q1"].pop(Automato.LAMBDACONSTANTE))
        
        

        novoAlfabeto = self.unirAlfabetos(vaiUnir)
        novoAutomato = self
        novoAutomato.alfabeto = novoAlfabeto
        # Junta os automatos self e vaiUnir
        for element in vaiUnir.funcTransf:
            novoAutomato.funcTransf[element] = vaiUnir.funcTransf[element]
        
        #Altera o estado inicial
        novoAutomato.funcTransf["q1"][Automato.LAMBDACONSTANTE] = estadoInicialAux
    
        #Altera o estado final
        novoAutomato.estadosFim = 'q{}'.format(quantidadeTotalEstados+1)

        # print("{} \n {}".format(self.funcTransf, vaiUnir.funcTransf))
        print(novoAutomato.estadosFim)
        return novoAutomato
    



    
trans_func = {'q1' : {'0' : ['q1', 'q2', 'q3'], '1' : ['q2']}, 'q2' : {'0' : ['q1'], '1' : ['q2']}}
a1 = Automato("q1", ["q2"], trans_func, ["0","1"]) #Palavras terminadas com 1

trans_func = {'q1' : {'1' : ['q2'], '0' : ['q3']}, 'q2' : {'0' : ['q2'], '1' : ['q2']}, 'q3' : {'0': ['q3'], '1': ['q3']}}
a2 = Automato("q1", ["q2"], trans_func, ["5","8", "0", "1"]) #palavras iniciadas com 1

trans_func = {'q1' : {'0' : ['q1', 'q2', 'q3'], '1' : ['q2']}, 'q2' : {'0' : ['q1'], '1' : ['q2']}}
a3 = Automato("q1", ["q2"], trans_func, ["0","1"]) #Palavras terminadas com 1

a1.unirAutomatos(a2)
#União entre o automato a1 e a2, gera transições lambdas. (necessário desenvolver uma estratégia p transformar AFN->AFD)
#Automato que começa com 1 ou termina com 1
print(a1.funcTransf)

a3.verificaPalavra("010000a0")

a3.verificaPalavra("0100000")

a3.verificaPalavra("01000001")


# a1.verificaPalavraRecursiva("00001", a1.funcTransf, a1.estadoIni, 0)


