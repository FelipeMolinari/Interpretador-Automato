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
    
    def adicionaEstadoSobLambda(self, estadosCorrente, transicao_func):
        auxiliar = []
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
                        

    def palavrasArquivo(self, arq):
        linhasValidas = []
        with open(arq, "r",encoding = "ISO-8859-1") as file:
            l = 1
            for linhas in file:
                palavra = ""
                for caracter in linhas:
                    if caracter != " " :
                        palavra += caracter
                    else:
                        i =0
                        for i in range(0, len(palavra)):
                            aux = palavra[i:len(palavra)]
                            
                            if self.maiorPalavraContida(aux) > 0:
                                
                                linhasValidas.insert(len(linhasValidas), l)
                        palavra = []
                l += 1
        linhasValidas = list(dict.fromkeys(linhasValidas)) 
        return linhasValidas  

            

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


    def criaNovoEstadoComTransicoesLambdas(self, estadoDest):

        for estado in self.funcTransf:
            if estado in self.estadosFim:

                self.funcTransf[estado][Automato.LAMBDACONSTANTE] = ['q{}'.format(estadoDest)]

        self.funcTransf['q{}'.format(estadoDest)]= {}

    def getQuantidadeDeEstados(self, aut2):
        return len(self.funcTransf) + len(aut2.funcTransf)

    def feixoKleene(self):
        
        novoAutomato = self
        for estado in self.estadosFim:
            novoAutomato.funcTransf[estado][Automato.LAMBDACONSTANTE] = [self.estadoIni]

        # novoAutomato.estadosFim.extend([self.estadoIni])
        return novoAutomato
   
    def concatenaAutomatos(self, vaiConcatenar):

        numEstadosSelfAutomato = len(self.funcTransf)
        quantidadeTotalEstados = len(self.funcTransf) + len(vaiConcatenar.funcTransf)

        #primeiro estado deve possuir q{valor} mair oque o ultimo q{valor} do automato self
        vaiConcatenar.alteraNomeEstados(numEstadosSelfAutomato)
        self.criaNovoEstadoComTransicoesLambdas(numEstadosSelfAutomato+1)

        novoAutomato = self
        # Junta os automatos self e vaiUnir
        novoAutomato.funcTransf.update(vaiConcatenar.funcTransf)
        #Altera o estado final
        novoAutomato.estadosFim = ['q{}'.format(quantidadeTotalEstados)]
        novoAutomato.estadoIni = "q1"
        
        return novoAutomato
    
    def unirAutomatos(self, vaiUnir):
        self.alteraNomeEstados(1)
        inicial = {Automato.LAMBDACONSTANTE:["q{}".format(2)]}
        self.funcTransf["q1"] = inicial

        numEstadosSelfAutomato = len(self.funcTransf)
        quantidadeTotalEstados = len(self.funcTransf) + len(vaiUnir.funcTransf)
        self.criaNovoEstadoComTransicoesLambdas(quantidadeTotalEstados+1)

        #primeiro estado deve possuir q{valor} mair oque o ultimo q{valor} do automato self
        vaiUnir.alteraNomeEstados(numEstadosSelfAutomato)

        vaiUnir.criaNovoEstadoComTransicoesLambdas(quantidadeTotalEstados+1)

        inicial = {Automato.LAMBDACONSTANTE:["q{}".format(numEstadosSelfAutomato+1)]}

        vaiUnir.funcTransf["q1"] = inicial
        
        estadoInicialAux = []
        estadoInicialAux.append(self.estadoIni)
        estadoInicialAux.append(vaiUnir.estadoIni)

        novoAutomato = self
        # Junta os automatos self e vaiUnir

        novoAutomato.funcTransf.update(vaiUnir.funcTransf)

        #Altera o estado inicial
        novoAutomato.funcTransf["q1"][Automato.LAMBDACONSTANTE] = estadoInicialAux
        novoAutomato.estadoIni = "q1"
    
        #Altera o estado final
        novoAutomato.estadosFim = ['q{}'.format(quantidadeTotalEstados+1)]
        return novoAutomato
   
