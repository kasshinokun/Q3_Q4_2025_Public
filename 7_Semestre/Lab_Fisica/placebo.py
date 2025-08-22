import streamlit as st
def lp_exercise():
    st.write("""
Considere os mecanismos de composição de tipos para as linguagens de programação. Escolha um, defina-o e mostre como o mesmo é implementado em um pequeno trecho de código de uma LP de sua preferência.

Sua resposta deve conter 4 componentes:

1) Mecanismo de composição escolhido;

2) Definição do mecanismo;

3) LP escolhida;

4) Trecho de código na LP escolhida.

Sua Resposta:
1) Mecanismo de composição: Conjunto potência 

2) Definição do mecanismo:

É o tipo de variáveis cujo valor pode ser qualquer 
subconjunto de um conjunto de elementos de um 
determinado tipo S, o qual é chamado tipo base 

3) LP escolhida: Python

4) Trecho de código em Python:
""")
    st.code("""
#==================================================

from enum import Enum

# Adaptado de Pascal

# Definindo os ingredientes como uma enumeração
Ingrediente = Enum('Ingrediente', ['FEIJAO', 'ARROZ', 'ALFACE', 'CENOURA', 'COUVE', 'CEBOLA'])

# Inicializando os conjuntos
sobras = {Ingrediente.ALFACE}

# Criando o conjunto salada com o intervalo de CENOURA até CEBOLA
# Primeiro, precisamos da lista de todos os ingredientes em ordem
todos_ingredientes = list(Ingrediente)
inicio = todos_ingredientes.index(Ingrediente.CENOURA)
fim = todos_ingredientes.index(Ingrediente.CEBOLA)
salada = set(todos_ingredientes[inicio:fim+1])

# Verificando a condição e atualizando o conjunto
if Ingrediente.FEIJAO not in sobras:
    salada = salada.union(sobras)

# Para visualização, podemos converter para nomes
print("Salada:", [ingrediente.name for ingrediente in salada])
print("Sobras:", [ingrediente.name for ingrediente in sobras])
#==================================================
# Saida no terminal:
# Salada: ['CEBOLLA', 'CENOURA', 'COUVE', 'ALFACE']
# Sobras: ['ALFACE']
""")

if not "__name__"in __name__:
    lp_exercise()
