import numpy as np
import math
import copy
from Automato import Automato

class FactoryAutomato:

    def __init__(self, tag):
        self.nome = ""
        self.definicao = ""
        self.tag = tag
    

    def defineNome(self):
        tagCmd = self.tag
        i = 0
        if("=" in tagCmd):
            while tagCmd[i]!="=":
                if tagCmd[i] != " ":
                    self.nome = "{}{}".format(self.nome,tagCmd[i])
                i = i+1

        return i+1


    def defineDefinicao(self, i):
        while i < len(self.tag):
            if self.tag[i] != " ":
                self.definicao = "{}{}".format(self.definicao,self.tag[i])
            i = i +1

    
    def getDefinicao(self):
        return self.definicao

    def getNome(self):
        return self.nome

    def tagValida(self):
        if ":" in self.tag[0]: return False
        i= self.defineNome()
        if len(self.nome) == 0 or self.nome is " " or i== len(self.tag): return False
        else:
            self.defineDefinicao(i); 
            return True
    
    def seTagValidaCriaAutomato(self):
        aux = None
        pilhaAutomato = []
        i=0
        while i< len(self.definicao):
            print(self.definicao[i])
            # Caractere de escape. '+' pode também ser um símbolo do alfabeto, basta adicionar o caracterer '\' antes do simbolo de operação
            if self.definicao[i] == "\\":        
                i =i + 2        
                pilhaAutomato.insert(len(pilhaAutomato),Automato.geraAutomatoComUmSimbolo(self.definicao[i]))
                continue
            # Caracter que faz a união entre dois automatos ab+
            if self.definicao[i] == "+":
                
                if len(pilhaAutomato) != 0:
                    aux = pilhaAutomato.pop()
                else:  
                    return False
                
                if len(pilhaAutomato) != 0:
                    self.automato = pilhaAutomato.pop()
                else:  
                    return False
                
                self.automato.unirAutomatos(aux)
                pilhaAutomato.insert(len(pilhaAutomato), self.automato)
            # Se ler o caracter '.' faz a concatenação de dois automatos. 
            elif self.definicao[i] == ".":
                if len(pilhaAutomato) != 0:
                    
                    aux = pilhaAutomato.pop()

                else:  
                    return False
                
                if len(pilhaAutomato) != 0:
                    self.automato = pilhaAutomato.pop()
                else:  
                    return False

                self.automato.concatenaAutomatos(aux)
                pilhaAutomato.insert(len(pilhaAutomato), self.automato)
            # Se ler o simbolo '*' faz a operação de kleene
            elif self.definicao[i] == "*":
                if len(pilhaAutomato) != 0:
                    self.automato = pilhaAutomato.pop()
                else:  
                    return False

                self.automato.feixoKleene()
                pilhaAutomato.insert(len(pilhaAutomato), self.automato)
            # Se ler um simbolo do alfabeto cria um automato com apenas um simbolo 
            else:
                pilhaAutomato.insert(len(pilhaAutomato),Automato.geraAutomatoComUmSimbolo(self.definicao[i]))
            i = i +1 

        if len(pilhaAutomato) == 0 or len(pilhaAutomato)>1: return False
        else: 
            self.automato = pilhaAutomato.pop()
            return True
