# Interpretador Automato

Trabalho realizado durante o perído 19.2 relacionado a disciplina de "Fundamentos Téoricos da Computação"
O objetivo do trabalho foi praticar os conceitos estudados em sala por meio da implementação de uma ferramente para fazer busca em arquivos de texto. 


### Pré-requisites

Possuir Python3 instalado no dispositivo.


## Comandos Disponíveis

Cria uma expressão regular e um nome para a mesma. Importante notar que a ER precisa estar na notação polonesa reversa. 
Ex: (a+b) -> ab+ para união, assim como a.b -> ab. para concatenação e a* para kleene.
```
nome = ER
```

---

Testa se uma str é aceita pelo automato representado pela expressão regular de nome passado como parâmetro.
```
:m m $'nome' "str"
```

---

Buca em um arquivo de texto todas as ocorrências das palavras que pertence a linguagem da expressão regular com nome passado como parâmetro.

```
:m m $'nome' "arquivo"
```

---

Lista todas as expressões regulares criadas pelo usuário.
```
:l
```

---

Interrompe o programa.
```
:p
```

### Ferramenta utilizada.

Código foi feito em python3 no visual code, não foi utilizado nenhuma biblioteca específica.

* [Visual Code](https://code.visualstudio.com/) - IDE utilizada
* [Python3](https://www.python.org/download/releases/3.0/) - Linguagem utilizada


## Qualquer dúvida:
felipemolinari874@gmail.com
