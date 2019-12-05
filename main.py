# Trabalho de FTC
# Montar um programa capaz de montar um automato através da expressão regular em sua forma "polonesa", Automato
# deve conseguir identificar se a palavra está contida no alfabeto.
# Felipe Cardoso Lima Molinari
# github.com/FelipeMolinari/Interpretador-Automato - felipemolinari874@gmail.com
# v3. 05/11
import numpy as np
import math
import copy
from FactoryAutomato import FactoryAutomato

def main():
    
    arrayDeTags = {}
    continuaLoop = True

    print("{}\n{}\n{}".format("****Interpretador AFN e AFD****","Felipe Carodos Lima Molinari - 15.1.8102, ****Projeto se encontra no repositorio****"))
    while continuaLoop:
        mensagemDeErro = ""
        comando = input("Por favor insira um comando: ")
        if len(comando) == 0:
            mensagemDeErro = "Desconsidera comandos vazios"
            
        elif len(comando) == 1:
            mensagemDeErro = "Desconsidera comandos com um caracter"

        else:         
            # São comandos da ferramenta 
            if comando[0]== ":":
                if comando[1] == "l":
                    print( "Listando o nome de todas as expressões regulares definidas:")
                    if(len(arrayDeTags) == 0):
                        print( "Ainda não foi adicionado nenhuma expressão regular.")
                    else: 
                        for tag in arrayDeTags:
                            print(tag)
                # Comando "f" recebe um arquivo e uma nome referênte à expressão regular, o retorno é as ocorrências de palavras aceitas pela expressão"
                elif comando [1] == "f":
                    if len(comando)<9:
                        mensagemDeErro = "Comando deve ser na forma => :m$'nomeExpressao'{}".format("nomeArquivo")
                    else: 
                        if not((comando[2] == " " and comando[3]== "$") or comando[2] == "$"):
                            mensagemDeErro = "Necessário utilizar o simbolo $ antes da especificação do nome da expressão"
                        else:
                            index1 = comando.index("'")
                            if index1 == 4 or index1 == 3:
                                segundaParteComando = comando[index1+1:len(comando)]
                                if "'" in segundaParteComando:
                                    index2 = segundaParteComando.index("'")
                                    tagNameEscolhida = comando[index1+1: index1 + index2 +1]
                                    if tagNameEscolhida in arrayDeTags:
                                        indexAux = index1
                                        index1 = comando.index('"')
                                        if index1< indexAux+ index2:
                                            mensagemDeErro = "Nome do arquivo deve vir depois do nome da expressão"
                                        else:
                                            segundaParteComando = comando[index1+1:len(comando)]
                                            if '"' in segundaParteComando:
                                                index2 = segundaParteComando.index('"')
                                                arquivoEscolhido = comando[index1+1: index1 + index2 +1]
                                                automato = arrayDeTags[tagNameEscolhida]["automato"]
                                                linhasValidas = automato.palavrasArquivo(arquivoEscolhido)
                                                if len(linhasValidas) == 0:
                                                    print("Nenhuma ocorrência encontrada")
                                                else: 
                                                    print("Foram encontrada ocorrência nas seguintes linhas...\n{}".format(linhasValidas))


                                            else: mensagemDeErro = "Necessário especificar o fim da palavra com aspas duplas"

                                    else: 
                                        mensagemDeErro = "Nome da expressão especificada não encontrada"
                                else: mensagemDeErro = "Necessário especificar fim do nome com aspas simples"
                            else: mensagemDeErro = "Comando deve ser na forma => :m$'nomeExpressa'{}".format('"nomeArquivo"')
                            
                    
                elif comando[1] == "m":
                    if len(comando)<9:
                        mensagemDeErro = "Comando deve ser na forma => :m$'nomeExpressa'{}".format("palavra a ser testada")
                    else: 
                        if not((comando[2] == " " and comando[3]== "$") or comando[2] == "$"):
                            mensagemDeErro = "Necessário utilizar o simbolo $ antes da especificação do nome da expressão"
                        else:
                            index1 = comando.index("'")
                            if index1 == 4 or index1 == 3:
                                segundaParteComando = comando[index1+1:len(comando)]
                                if "'" in segundaParteComando:
                                    index2 = segundaParteComando.index("'")
                                    tagNameEscolhida = comando[index1+1: index1 + index2 +1]
                                    if tagNameEscolhida in arrayDeTags:
                                        indexAux = index1
                                        index1 = comando.index('"')
                                        if index1< indexAux+ index2:
                                            mensagemDeErro = "Palavra a ser testada deve vir depois do nome da expressão"
                                        else:
                                            segundaParteComando = comando[index1+1:len(comando)]
                                            if '"' in segundaParteComando:
                                                index2 = segundaParteComando.index('"')
                                                tagPalavraEscolhida = comando[index1+1: index1 + index2 +1]
                                                automato = arrayDeTags[tagNameEscolhida]["automato"]
                                                maiorPalavraAceita = tagPalavraEscolhida[0:automato.maiorPalavraContida(tagPalavraEscolhida)]
                                                print("Aceita até: {}".format(maiorPalavraAceita))
                                                if len(maiorPalavraAceita) == 0:
                                                    print("Palavra não é aceita")
                                                elif len(maiorPalavraAceita) == len(tagPalavraEscolhida):
                                                    print("Palavra é aceita por completo")
                                                else: print("Palavra é parcialmente aceita")

                                            else: mensagemDeErro = "Necessário especificar o fim da palavra com aspas duplas"

                                    else: 
                                        mensagemDeErro = "Nome da expressão especificada não encontrada"
                                else: mensagemDeErro = "Necessário especificar fim do nome com aspas simples"
                            else: mensagemDeErro = "Comando deve ser na forma => :m$'nomeExpressa'{}".format("palavra a ser testada")
                            
                elif "q" in comando[1]:
                    continuaLoop = False    
            
            # É uma Factory Automato
            else:
                aut = FactoryAutomato(comando)
                if aut.tagValida():
                    if aut.getNome() not in arrayDeTags:
                        if aut.seTagValidaCriaAutomato():

                            arrayDeTags[aut.getNome()] = {}
                            arrayDeTags[aut.getNome()]["expressao"] = aut.getDefinicao()
                            arrayDeTags[aut.getNome()]["automato"] = aut.automato
                            print("Expressão regular definida corretamente... {}".format(aut.getDefinicao()))
                        else:
                            mensagemDeErro = "Sua expressão precisa estar na forma da notação polonesa."

                    else:
                            mensagemDeErro = "Nome dado à expressão já existe."
                else:
                    mensagemDeErro = "Erro nos dados da especificados. Usar nome = expressaoPolonesa"
                    
        if len(mensagemDeErro)!=0:
            print("***Comando Inválido***\nDescrição do erro: {}".format(mensagemDeErro) )

    

if __name__ == "__main__":
    main()

