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
    
    arrayDeTags = []
    continuaLoop = True

    while continuaLoop:
        comando = input("Por favor insira um comando: ")
        if len(comando) == 0:
            print("Insira um comando válido")
            continue
        elif len(comando) == 1:
            print("Insira um comando válido")
            continue
        
        # São comandos da ferramenta 
        elif comando[0]== ":":
            if comando[1] == "l":
                print( "Listando o nome de todas as expressões regulares definidas:")
                if(len(arrayDeTags) == 0):
                    print( "Ainda não foi adicionado nenhuma expressão regular.")
                else: 
                    for tag in arrayDeTags:
                        print(tag)

            elif "q" in comando[1]:
                continuaLoop = False    
        
        # É uma Factory Automato
        else:
            aut = FactoryAutomato(comando)
            if(aut.tagValida()):
                if aut.seTagValidaCriaAutomato():
                    arrayDeTags.insert(len(arrayDeTags), aut.getNome())
                    print("Expressão regular definida corretamente... {}".format(aut.getDefinicao()))

                else:
                    print("Sua expressão deve estar na notação polonesa.")
            else:
                print("Digite um comando certo para criar uma expressão regular, por exemplo: (nome = ab+c.)")
                
            


    

if __name__ == "__main__":
    main()