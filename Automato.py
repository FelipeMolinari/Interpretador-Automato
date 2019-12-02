# Trabalho de FTC
# Montar um programa capaz de montar um automato através da expressão regular em sua forma "polonesa", Automato
# deve conseguir identificar se a palavra está contida no alfabeto.
# Felipe Cardoso Lima Molinari
# github.com/FelipeMolinari/Interpretador-Automato - felipemolinari874@gmail.com
# v3. 05/11
import numpy as np
import math
import copy

class Automato:

    LAMBDACONSTANTE = "lambda"

    def __init__(self, estadoIni , estadosFim, funcTransf):
        self.estadoIni = estadoIni
        self.estadosFim = estadosFim
        self.funcTransf = funcTransf
        self.estadoAtual = estadoIni
    
            
    # trans_func = {'q1' : {'0' : ['q1', 'q2', 'q3'], '1' : ['q2']}, 'q2' : {'0' : ['q1'], '1' : ['q2']}}

             
# Primeiro: verifico qual simbolo
# Segundo: Verifico no meu conjunto de estados correntes qual o proximo estado para aquele simbolo
# Terceiro: Altero o meu estado corrente para o novo

# trans_func = {'q1' : {'0' : ['q1', 'q2'], '1' : ['q2']}, 'q2' : {'0' : ['q1'], '1' : ['q2']}}

    def adicionaEstadoSobLambda(self, estadosCorrente, transicao_func):


        auxiliar = []
        # print('Então .... {}'.format(transicao_func))
        # input('{}'.format(estadosCorrente))
        
        for element in estadosCorrente:
            if(Automato.LAMBDACONSTANTE in transicao_func[element]):       
                    auxiliar.extend(transicao_func[element][Automato.LAMBDACONSTANTE])
        estadosCorrente.extend(auxiliar)
        estadosCorrente = list(dict.fromkeys(estadosCorrente)) 
        return estadosCorrente          

    def maiorPalavraContida(self, palavra):

        conjuntoEstadoCorrente = []
        conjuntoEstadoCorrente.append(self.estadoIni)
        auxiliar = []
        transicao_func = self.funcTransf
        contadorDeTransicoes = 0

        if self.estadoIni in self.estadosFim:
            aceitaAte = 1
        else: aceitaAte = 0

        for simbolo in palavra:   
            conjuntoEstadoCorrente = self.adicionaEstadoSobLambda(conjuntoEstadoCorrente, transicao_func )

            for element in conjuntoEstadoCorrente: 

                if simbolo in transicao_func[element]:
                    auxiliar.extend(transicao_func[element][simbolo])
                
                        
            auxiliar = self.adicionaEstadoSobLambda(auxiliar, transicao_func )
            auxiliar = list(dict.fromkeys(auxiliar)) #Remove os elementos duplicados
            
            contadorDeTransicoes +=1

            if len(auxiliar) != 0:
                for elem in auxiliar:
                    if elem in self.estadosFim:
                        aceitaAte = contadorDeTransicoes
                        break                    
            else: 
                return aceitaAte
            
            
            conjuntoEstadoCorrente = copy.deepcopy(auxiliar)
            
            auxiliar = []
        return aceitaAte
                        



    #Gera um automato que aceita apenas um simbolo
    @staticmethod
    def geraAutomatoComUmSimbolo(simbolo):
        trans_func_novo = {'q1' : {'{}'.format(simbolo) : ['q2']}, 'q2':{}}
        novoAutomato = Automato("q1", ["q2"], trans_func_novo)
        return novoAutomato


# Altera os nomes dos estados do automato passado como parâmetro. Operações de união, concatenação ou Kleene utiliza essa função.
# numEstados: Variável que define o número do primeiro estado do automato.
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
        self.estadoIni = 'q{}'.format(int(self.estadoIni[1]) + numEstados)

        # Muda também o nome dos estados finais
        
        for x in range(len(self.estadosFim)):
            self.estadosFim[x] = 'q{}'.format(int(self.estadosFim[x][1]) + numEstados)

        # inicial = {Automato.LAMBDACONSTANTE:"q{}".format(numEstados+1)}
        # self.funcTransf["q1"] = inicial


    def criaNovoEstadoComTransicoesLambdas(self, estadoDest):

        for estado in self.funcTransf:

            if estado in self.estadosFim:
                self.funcTransf[estado][Automato.LAMBDACONSTANTE] = ['q{}'.format(estadoDest)]

        self.funcTransf['q{}'.format(estadoDest)]= {
            Automato.LAMBDACONSTANTE:['q{}'.format(estadoDest)]
        }

        
       

    def getQuantidadeDeEstados(self, aut2):
        return len(self.funcTransf) + len(aut2.funcTransf)


    def concatenaAutomatos(self, vaiConcatenar):
        self.alteraNomeEstados(0)

        numEstadosSelfAutomato = len(self.funcTransf)
        quantidadeTotalEstados = len(self.funcTransf) + len(vaiConcatenar.funcTransf)

        #primeiro estado deve possuir q{valor} mair oque o ultimo q{valor} do automato self
        vaiConcatenar.alteraNomeEstados(numEstadosSelfAutomato)
        
        self.criaNovoEstadoComTransicoesLambdas(numEstadosSelfAutomato+1)

        novoAutomato = self
        # Junta os automatos self e vaiUnir
        novoAutomato.funcTransf.update(vaiConcatenar.funcTransf)

        #Altera o estado final
        novoAutomato.estadosFim = 'q{}'.format(quantidadeTotalEstados)
        novoAutomato.estadoIni = "q1"
        return novoAutomato
    
    


    def unirAutomatos(self, vaiUnir):
        self.alteraNomeEstados(1)
        inicial = {Automato.LAMBDACONSTANTE:["q{}".format(2)]}
        self.funcTransf["q1"] = inicial

        numEstadosSelfAutomato = len(self.funcTransf)
        quantidadeTotalEstados = len(self.funcTransf) + len(vaiUnir.funcTransf)

        #primeiro estado deve possuir q{valor} mair oque o ultimo q{valor} do automato self
        vaiUnir.alteraNomeEstados(numEstadosSelfAutomato)
        
        inicial = {Automato.LAMBDACONSTANTE:["q{}".format(numEstadosSelfAutomato+1)]}

        vaiUnir.funcTransf["q1"] = inicial
        
        self.criaNovoEstadoComTransicoesLambdas(quantidadeTotalEstados+1)
        vaiUnir.criaNovoEstadoComTransicoesLambdas(quantidadeTotalEstados+1)

        # estado inicial q1 deve possuir trasição lambda para ambos os automatos
        
        estadoInicialAux = []
        estadoInicialAux.append(self.estadoIni)
        estadoInicialAux.append(vaiUnir.estadoIni)

        novoAutomato = self
        # Junta os automatos self e vaiUnir

        novoAutomato.funcTransf.update(vaiUnir.funcTransf)
        # for element in vaiUnir.funcTransf:
        #     novoAutomato.funcTransf[element] = vaiUnir.funcTransf[element]
        
        #Altera o estado inicial
        novoAutomato.funcTransf["q1"][Automato.LAMBDACONSTANTE] = estadoInicialAux
        novoAutomato.estadoIni = "q1"
    
        #Altera o estado final
        novoAutomato.estadosFim = ['q{}'.format(quantidadeTotalEstados+1)]

        # print("{} \n {}".format(self.funcTransf, vaiUnir.funcTransf))
        return novoAutomato
    
    
# trans_func2 = {'q1' : {'0' : ['q2']}, 'q2' : {}}

# trans_func = {'q1' : {'a' : ['q2']}, 'q2' : {}}

# a2 = Automato("q1", ["q2"], trans_func)
# a1 = Automato("q1", ["q2"], trans_func2) 
# automatoConcatenado = a1.concatenaAutomatos(a2)
a1 = Automato.geraAutomatoComUmSimbolo("a")
a2 = Automato.geraAutomatoComUmSimbolo("b")
a3 = a1.unirAutomatos(a2)
a4 = Automato.geraAutomatoComUmSimbolo("b")
a5 = a3.concatenaAutomatos(a4)
print(a5.maiorPalavraContida('ab555'))





































































    # def verificaPalavraRecursao(self, palavra,funcTransf, estado, simbolo):

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
