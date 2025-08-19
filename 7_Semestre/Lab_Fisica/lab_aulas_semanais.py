
# Interface
import streamlit as st
# Listas e Matrizes
import pandas as pd
import numpy as np
# Calculos
import numbers
import math
# Listas
from typing import List
# IO e Imagens
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import base64
from io import BytesIO
import json

def plot_caixa():
    # Configurar contexto para evitar interferências
    with plt.ioff():
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Definição dos vértices da caixa
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # base
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # topo
        ])

        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[1], vertices[2], vertices[6], vertices[5]],
            [vertices[4], vertices[7], vertices[3], vertices[0]]
        ]

        # Plotar faces com cores específicas
        poly3d = Poly3DCollection(
            faces,
            facecolors=['lightblue', 'lightblue', 'skyblue', 'skyblue', 'skyblue', 'lightblue'],
            linewidths=1,
            edgecolors='k',
            alpha=0.9
        )
        ax.add_collection(poly3d)
    # Adicionar rótulos
        ax.text(0.5, -0.1, 0, 'A', fontsize=12) # type: ignore (Pylance com falso-negativo)
        ax.text(1.05, 0.5, 0, 'B', fontsize=12) # type: ignore (Pylance com falso-negativo)
        ax.text(-0.05, 0.5, 0.5, 'C', fontsize=12) # type: ignore (Pylance com falso-negativo)

        # Configurar aspecto visual
        ax.set_box_aspect([1.0, 1.0, 1.0]) # type: ignore (Pylance com falso-negativo)
        ax.set_axis_off()
        ax.set_xlim([-0.1, 1.1]) # type: ignore (Pylance com falso-negativo)
        ax.set_ylim([-0.1, 1.1]) # type: ignore (Pylance com falso-negativo)
        ax.set_zlim([-0.1, 1.1]) # type: ignore (Pylance com falso-negativo)
        # Renderizar no Streamlit
        st.pyplot(fig)
        
    # Fechar figura explicitamente
    plt.close(fig)

def plot_triangulo():
    fig, ax = plt.subplots()
    ax.plot([0, 4], [0, 0], 'k')  # base
    ax.plot([0, 4], [0, 3], 'k')  # hipotenusa
    ax.plot([4, 4], [0, 3], 'k')  # altura

    # Marcar ângulo θ
    angulo = np.linspace(0, np.pi/6, 50)
    ax.plot(0.5*np.cos(angulo), 0.5*np.sin(angulo), 'k')
    ax.text(0.3, 0.05, r'$\theta$', fontsize=14)

    ax.axis('equal')
    ax.axis('off')
    st.pyplot(fig)

def verify_key_json(path_json: str, key: str) -> bool:
    """Verifica se uma chave existe em um arquivo JSON."""
    try:
        with open(path_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            return key in data
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    except Exception as e:
        st.error(f"Erro inesperado em verify_key_json: {e}")
        return False


def write_json(path_json: str, path_image: str, name_image: str):
    """Adiciona imagem codificada em Base64 ao JSON apenas se a chave ainda não existir."""
    try:
        # Carregar dados existentes ou iniciar dicionário vazio
        try:
            with open(path_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Só adiciona se a chave não existir
        if name_image not in data:
            with open(path_image, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode("utf-8")
            data[name_image] = img_base64

            with open(path_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            st.info(f"A chave '{name_image}' já existe no JSON. Nenhuma alteração feita.")

    except FileNotFoundError:
        st.error(f"Imagem não encontrada: {path_image}")
    except Exception as e:
        st.error(f"Erro ao escrever JSON: {e}")


def read_json(path_json,name_image):
    # 1. Ler o arquivo JSON
    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Decodificar a imagem
    image_bytes = base64.b64decode(data[name_image])

    return image_bytes
def test():
    
    try:
        write_json("image.json","images/concept01/image.png","image1.png")
        write_json("image.json","images/concept02/image2.png","image2.png")
        write_json("image.json","images/concept02/image3.png","image3.png")
        write_json("image.json","images/concept02/image4.png","image4.png")
        write_json("image.json","images/concept02/image5.png","image5.png")
        write_json("image.json","images/concept02/image6.png","image6.png")
        write_json("image.json","images/concept02/image7.png","image7.png")
        write_json("image.json","images/activity02/image8.png","image8.png")
        write_json("image.json","images/activity02/image9.png","image9.png")
        for i in range(len(["image1.png","image2.png","image3.png","image4.png","image5.png","image6.png","image7.png","image8.png","image9.png"])):
            st.image(BytesIO(read_json("image.json",f"image{i+1}.png")),
                        caption=f"Figura {i+1}",
                        use_container_width=True)
    except Exception as e:
        st.error(f"Erro: {e}")

def Introduction():
    # --- Page Title ---
    st.header("DETERMINAÇÃO DO TEMPO DE REAÇÃO DE UMA PESSOA")

    # --- Introduction Section ---
    st.subheader("INTRODUÇÃO")
    st.write("Cada pessoa reage a um dado estímulo após um certo tempo. O intervalo de tempo entre a percepção de um estímulo externo e a resposta (ou reação) motora é chamado de tempo de reação.")
    st.write("Os estímulos externos podem ser percebidos através do sistema sensorial, responsável pelo tato, paladar, visão, olfato e audição.")
    st.write("Exemplos:")
    st.markdown(
        """
    - Um atleta de natação treina a largada com um estímulo sonoro (um apito). Quanto menor for o tempo de reação, maiores as chances de vencer.
    - Um piloto de Fórmula 1 treina a reação a um estímulo visual, pois a largada se dá através de luzes que se apagam.
    """
    )
    st.write("O tempo de reação de uma pessoa depende do sistema sensorial que está sendo acionado.")
    st.write("O tempo de reação também depende de fatores fisiológicos, condicionamento físico, idade, sexo e estado emocional.")

    # --- Experimental Part Section ---
    st.subheader("PARTE EXPERIMENTAL")

    st.subheader("Objetivo")
    st.write("Determinar o tempo de reação de um grupo de alunos.")

    st.subheader("Material Utilizado")
    st.write("Uma régua milimetrada.")

    st.subheader("Procedimento")
    st.write("Esta prática consiste em estimar o tempo de reação de uma pessoa através de um estímulo visual.")
    st.write("O procedimento é o seguinte:")
    st.markdown(
        """
    1. Uma pessoa (A) mantém a mão na posição horizontal, por exemplo, com o antebraço apoiado em uma mesa.
    2. Outra pessoa (B) segura uma régua com a marca do zero entre o indicador e o polegar da pessoa A.
    3. Sem aviso, a pessoa B solta a régua. A pessoa A deve segurá-la o mais rápido possível, mantendo o braço no mesmo nível.
    4. A distância ($h$) que a régua cai antes de ser pega é medida.
    """
    )
    #link="https://files.passeidireto.com/034cda0f-96b7-4ad2-a954-476b843ed4dd/bg5.png"
    # --- Display the image ---
    
    
    st.image(BytesIO(read_json("image.json","image1.png")), 
             caption="Figura 1: Representação do procedimento para determinação do tempo de reação de uma pessoa através de um estímulo visual.", 
             use_container_width=True)
    # You would need to replace "path/to/your/image.png" with the actual path to the image file.
    # Since the image is part of a PDF, you would first need to extract it and save it as an image file.

    # --- Physics Formula Section ---
    st.subheader("Análise Física")
    st.write("Considerando que a régua cai sob ação apenas da força gravitacional, a posição vertical do 'zero' da régua é dada pela expressão:")
    st.latex(r"y(t)=y_{0}+v_{0y}t-\frac{1}{2}gt^{2}")
    st.write("Onde:")
    st.markdown(
        """
    - O eixo $y$ é considerado positivo para cima.
    - $y_{0}$ é a posição inicial, que é 0 m.
    - $v_{0y}$ é a velocidade inicial, que também é 0 m/s, pois a régua é solta.
    - $g = 9.8 m/s^2$ é a aceleração gravitacional.
    """
    )
    st.write("Portanto, a equação do movimento da régua se reduz a:")
    st.latex(r"y(t)=-\frac{1}{2}gt^{2}")
    st.write("O tempo de reação ($t_r$) é o tempo que a pessoa leva para segurar a régua. Nesse instante, a régua caiu uma distância $h$, o que significa que sua posição final é $y=-h$.")
    st.write("Substituindo $y=-h$ e $t=t_r$ na equação, obtemos:")
    st.latex(r"-h=-\frac{1}{2}gt_{r}^{2}")
    st.write("Isolando $t_r$ da equação, a expressão para estimar o tempo de reação é:")
    st.latex(r"t_{r}=\sqrt{\frac{2h}{g}}")
def concept_01():
    st.subheader("MEDIÇÕES E INCERTEZAS")
    st.subheader("INTRODUÇÃO")
    st.markdown(
        """
        A Física, como as outras ciências, se baseia na observação sistemática de fenômenos naturais para sustentar teorias. 
        As leis da Física são as ferramentas usadas para explicar a dinâmica e a relação entre as grandezas físicas, que são quantidades que podem ser mensuradas. Para que os resultados das medições sejam reprodutíveis, as leis da Física dependem de métodos de medição e procedimentos rigorosos.

        O resultado de uma medição deve incluir o valor da grandeza, a incerteza e a unidade. No Brasil, o sistema legal de unidades é o Sistema Internacional (SI) e as regras para expressar os resultados e incertezas são definidas pela ABNT e pelo INMETRO.

        Todas as medições de grandezas físicas são afetadas por incertezas, que podem ser causadas pelo processo de medição, equipamentos, variáveis não medidas e até mesmo pelo operador. Embora a incerteza possa ser minimizada pela perícia do operador, ela jamais pode ser eliminada. Quanto menor o valor da incerteza, mais confiável ou preciso é o resultado. Os resultados das medições devem ser expressos de forma que a precisão possa ser avaliada. A maneira mais comum de expressar o resultado da medição de uma grandeza $x$ é $(x \\pm \\Delta x)$ [unidade], onde $\\Delta x$ é a incerteza. A incerteza $\\Delta x$ deve ter, no máximo, dois algarismos significativos.

        Existem diferentes métodos para estimar o valor de $\\Delta x$. A escolha do método depende dos procedimentos de medição e se a medição é direta ou indireta. Uma medição é direta quando o resultado é lido diretamente do instrumento, e indireta quando é obtido a partir de medições de outras grandezas e da relação funcional entre elas.

        **Algarismos Significativos**
        * O algarismo zero só é significativo se estiver à direita de um algarismo significativo.
        * Exemplo: $0,00082$ tem apenas dois algarismos significativos (8 e 2).
        * Exemplo: $80200$ tem cinco algarismos significativos.
        * Exemplo: $0,000802$ tem três algarismos significativos.

        **Parte Experimental**
        **Objetivo:** Determinar o tempo de queda de uma esfera com sua incerteza e avaliar a precisão e acurácia do resultado.
        **Material:** Esfera, cronômetro e régua.
        """
    )
    st.header("PROCEDIMENTOS")
    st.markdown(
        """
        1. Abandone a esfera de uma altura $h$ e meça o tempo $t$ de queda. Recomenda-se repetir o procedimento 10 vezes devido à dependência do reflexo do operador. Anote os resultados na Tabela 1.
        """
    )

    st.subheader("Tabela 1: Tempo de queda de uma esfera medido 10 vezes")

    cols_t = st.columns(3)
    # Inputs (garanta chaves únicas)
    t_values: List[float] = [
            float(cols_t[i % 3].number_input(f"t{i+1} (s)", key=f"t{i+1}", format="%.3f", value=0.0,step=0.001))
        for i in range(10)
    ]
    # Exibe tabela 1
    tabela1_df = pd.DataFrame({"$t(s)$": t_values}, index=[f"{i+1}" for i in range(10)])
    st.table(tabela1_df.T)


    st.markdown(
        """
        2. Determine o valor mais provável para o tempo de queda através da média aritmética:
        """
    )
    st.latex(r"t_{med} = \frac{1}{n}\sum_{i=1}^{n}t_{i}")
    t_values_filtered = [val for val in t_values if val is not None]
    if t_values_filtered:
        t_med = np.mean(t_values_filtered)
        st.write(f"$t_{{med}} = {t_med:.4f}$ s")
    else:
        st.write("$t_{med}$ =")

    st.markdown(
        """
        3. A incerteza $\\Delta t$ da medição é identificada com o desvio padrão, definido como:
        """
    )
    st.latex(r"\Delta t = \frac{1}{n}\sum_{i=1}^{n}|t_{med}-t_{i}")

    if t_values_filtered:
        delta_t = np.sum(np.abs(np.array(t_values_filtered) - t_med)) / len(t_values_filtered)
        st.write(f"$\\Delta t = {delta_t:.5f}$ s")
        st.markdown(
            f"O resultado deve ser expresso como $(t_{{med}} \\pm \\Delta t)$ [unidade]. Por exemplo, se $t = (0,62 \\pm 0,11)$ s, seria incorreto expressar como $(0,62 \\pm 0,1128)$ s, pois a incerteza deve ter no máximo dois algarismos significativos. Se o algarismo a ser abandonado for 5 ou maior, adicione uma unidade ao algarismo que permaneceu. Também seria incorreto expressar como $(0,6185 \\pm 0,11)$ s, pois a precisão do resultado não deve ser maior do que a da incerteza."
        )
    else:
        st.write("$\\Delta t$ =")

    st.markdown(
        """
        4. Anote na Tabela 2 os resultados para $t_{med}$ e $\\Delta t$ de cada grupo. O resultado mais preciso é aquele com o menor desvio médio percentual ($\\epsilon$), que é definido como:
        """
    )
    st.latex(r"\epsilon=\frac{\Delta t}{t_{med}}\times100")

    st.subheader("Tabela 2")
    st.markdown(
        "Tempo médio ($t_{med}$), desvio médio ($\\Delta t$) e desvio médio percentual ($\\epsilon$) de cada grupo. Gravidade ($g$) e seu desvio percentual em relação ao valor esperado ($\\Delta g$)."
    )

    num_groups = st.slider("Número de grupos", 1, 4, 1)
    
    table2_data = {
        "Grupo": [f"{i+1}" for i in range(num_groups)],
        "$t_{med}(s)$": [None] * num_groups,
        "$\\Delta t(s)$": [None] * num_groups,
        "$\\epsilon(\\%)$": [None] * num_groups,
        "$g(m/s^{2})$": [None] * num_groups,
        "$\\Delta g(\\%)$": [None] * num_groups,
    }
    
    tabela2_df = pd.DataFrame(table2_data).set_index("Grupo")
    cols = st.columns(num_groups)    
    for i in range(num_groups):
        with cols[i]:
            # Adaptação para evitar de zerar epsilon no momento errado(Pylance Tentativa 4)
            input1=st.number_input(f"Grupo {i+1} - $t_{{med}}(s)$", 
                                    key=f"tmed_group_{i+1}",
                                    step=0.001,
                                        format="%.3f"
                                    )
            tabela2_df.loc[f"{i+1}", "$t_{med}(s)$"] = input1
            input2=st.number_input(f"Grupo {i+1} - $\\Delta t(s)$", 
                                    key=f"deltat_group_{i+1}",
                                step=0.001,
                                    format="%.3f"
                                )
            tabela2_df.loc[f"{i+1}", "$\\Delta t(s)$"] = input2
            # Epsilon=(delta_t/t_medio)*100
            tabela2_df.loc[f"{i+1}","$\\epsilon(\\%)$"] = (float(input2)/float(input1)) *100 if not(input1==0 and input2==0) else 0
    
        # Calculate epsilon
    # Calculate epsilon(Pylance apresentou falso-negativo)
    # Tentativa 3 - Falso-negativo Pylance 
    #tabela2_df["$t_{med}(s)$"] = tabela2_df["$t_{med}(s)$"].astype(float)
    #tabela2_df["$\\Delta t(s)$"] = tabela2_df["$\\Delta t(s)$"].astype(float)

    #tabela2_df["$\\epsilon(\\%)$"] = (
     #   tabela2_df["$\\Delta t(s)$"] / tabela2_df["$t_{med}(s)$"]
    #).replace([np.inf, -np.inf], np.nan).round(5) * 100

        
    # Tentativa 2 - Falso-negativo Pylance (mais simples e estável)
    #if not(tabela2_df["$t_{med}(s)$"].isna or tabela2_df["$t_{med}(s)$"]=="0.000"):
        #tabela2_df["$\\epsilon(\\%)$"] = (tabela2_df["$\\Delta t(s)$"] / tabela2_df["$t_{med}(s)$"])*100
    #else:
        #st.error("Coloque valores diferentes de zero.")
        #tabela2_df["$\\epsilon(\\%)$"] = 0
    #----------------------------> Código original(Tentativa 1)
    #for i in range(num_groups):
        #t_med_val = tabela2_df.loc[f"{i+1}", "$t_{med}(s)$"]
        #delta_t_val = tabela2_df.loc[f"{i+1}", "$\\Delta t(s)$"]
        
        #if t_med_val is not None and delta_t_val is not None and t_med_val != 0.0:                                  
            #epsilon = (delta_t_val/t_med_val)*100
            #tabela2_df.loc[f"{i+1}", "$\\epsilon(\\%)$"] = f"{epsilon:.5f}"
    #-----------------------------> Fim
    
    st.table(tabela2_df)


    st.markdown(
        """
        5. O resultado mais acurado (mais próximo do valor verdadeiro) pode ser obtido usando a expressão matemática que relaciona a posição de um corpo em movimento uniformemente acelerado e o tempo: 
        """
    )
    st.latex(r"h=\frac{gt^{2}}{2}")
    h_value = st.number_input("Altura h (m)", value=0.93,step=0.01)
    
    st.markdown(
        """
        Calcule o valor de $g$ e o desvio percentual em relação ao valor esperado (9,8 m/s²), definido como:
        
        """
    )
    st.latex(r"\Delta g=\frac{|g-9,8|}{9,8}x~100")
    tabela2_df_updated = tabela2_df.copy()
    
    # Calculate g and Delta g
    for i in range(num_groups):
        t_med_val = tabela2_df.loc[f"{i+1}", "$t_{med}(s)$"]
        # Verifica se são números reais e não NaN
        if (
            isinstance(t_med_val, numbers.Real)
            and isinstance(h_value, numbers.Real)
            and not np.isnan(h_value)
            and tabela2_df.loc[f"{i+1}", "$t_{med}(s)$"] !=np.nan
            and t_med_val != 0
        ):
            # h=(1/2)*g*t^2
            # e g=2*h/(t^2)
            g = (2 * h_value) / pow(float(t_med_val),2)
            # g = (2 * h_value) / (float(t_med_val)*float(t_med_val))
            # g = (2 * h_value) / (float(t_med_val)**2)
            tabela2_df_updated.loc[f"{i+1}", "$g(m/s^{2})$"] = f"{g:.2f}"
            delta_g = (np.abs(g - 9.8) / 9.8) * 100
            tabela2_df_updated.loc[f"{i+1}", "$\\Delta g(\\%)$"] = f"{delta_g:.2f}"
        else:
            st.error("Coloque valores diferentes de zero.")
            tabela2_df_updated.loc[f"{i+1}", "$g(m/s^{2})$"] = None
            tabela2_df_updated.loc[f"{i+1}", "$\\Delta g(\\%)$"] = None

    st.table(tabela2_df_updated)

    st.markdown("O resultado com o menor desvio percentual em relação ao valor esperado é o mais acurado.")
def concept02():
    
    st.subheader("MEDIDAS DIRETAS, INDIRETAS E PROPAGAÇÃO DE ERROS")
    st.markdown("""
    **Introdução – Medições Diretas**

    Imagine que você esteja realizando uma medida do comprimento de um lápis usando uma régua 
    com menor divisão de 0,1 cm. O comprimento observado está entre 3,7 e 3,8 cm. Devido a resolução da 
    régua não é possível ter garantia exata sobre a medida do comprimento do lápis. A informação de 
    medida mais adequada nesse caso seria expressar como **3,75 cm ± 0,05 cm** (metade da menor divisão).

    Observe que estamos seguros em relação aos algarismos 3 e 7 pois eles foram obtidos 
    através de divisões inteiras da régua, ou seja, você tem certeza deles. Entretanto, o algarismo 5 foi 
    avaliado, isto é, você não tem certeza sobre seu valor e outra pessoa poderia avaliá-lo como sendo 
    4 ou 6, por exemplo. Por isso, esse algarismo avaliado é denominado algarismo duvidoso. """)
    
    st.image(BytesIO(read_json("image.json", "image2.png")),
             caption="Figura 1 – Comprimento de um lápis com régua e a incerteza", use_container_width=True)
                
    st.markdown("""
    Algarismos certos são obtidos diretamente da escala, enquanto o algarismo duvidoso é estimado.  
    Duas medidas como `87 cm` e `87,0 cm` não são equivalentes, pois a segunda indica que o zero 
    é o algarismo duvidoso.  Do mesmo modo, resultados como 2,44 𝑐𝑚 e 2,46 𝑐𝑚, por exemplo, não 
    são fundamentalmente diferentes, pois diferem apenas no algarismo duvidoso. 
    
    ***IMPORTANTE:***
    Quando se realiza uma única medida de uma grandeza, a incerteza pode ser encontrada 
    usando-se diferentes procedimentos, mas é sempre importante usar-se o bom senso. Uma regra 
    amplamente difundida é a de que a incerteza de uma medida isolada (erro de leitura) deve ser a 
    metade da menor divisão da escala do instrumento de medida.
                
    **Medições Únicas**
                
    Em medições únicas, a incerteza normalmente é metade da menor divisão do instrumento, mas 
    deve-se ter cuidado com medições que exigem reposicionar o instrumento várias vezes, pois a 
    incerteza aumenta.
    O valor mais provável da grandeza é dado por:""")

    st.latex(r"y = \frac{y_{max} + y_{min}}{2}")
    st.markdown("""e a incerteza padrão, estimada como desvio padrão dessa distribuição, é dada por:""")
    st.latex(r"\Delta y = \frac{y_{max} - y_{min}}{2\sqrt{3}}")
    st.markdown(f""" O fator """+"$${\\sqrt{3}}$$"+ """ decorre da distribuição retangular de probabilidade [2].""")
    
    st.markdown("""
    No caso de aparelhos digitais, a avaliação do desvio deverá ser feita como no caso anterior, 
    através dos limites de oscilação, se houver oscilação, ou através da própria precisão do 
    instrumento, se não houver oscilação. No caso de não se ter a informação da precisão do 
    instrumento, pode-se considerar 3%. 
    O desvio relativo é a razão entre a incerteza ∆𝑦 e o valor médio de y,""")  
    st.latex(r"\frac{\Delta y}{y}")
    st.markdown("""O desvio percentual é o desvio relativo expresso em percentual,""") 
    st.latex(r"\frac{\Delta y}{y}\times 100 \%")
    st.markdown("""Os desvios percentuais permitem comparar as precisões das medidas.""")
    
    st.markdown("""
    **Medições Indiretas e Propagação de Erros**

    Muitas grandezas não podem ser medidas diretamente, sendo calculadas a partir de outras 
    medições de N outras grandezas físicas e da relação funcional:""")
    st.latex(r'''y = f(x_1, x_2, \dots, x_N)''')
    st.markdown(""" 
    
    É fundamental calcular e expressar a incerteza associada ao resultado, ou seja, qual é a 
    consequência da propagação das incertezas.

    Algumas regras úteis para propagação de incertezas:

    1. **Soma/Subtração**:""")
    
    st.latex(r'''\Delta y = \Delta a + \Delta b + \dots + \Delta n''')
    st.markdown(""" 2. **Multiplicação por constante**: Δy = k·Δa""")
    
    st.latex(r'''\Delta y = k \times \Delta a''')
    
    st.markdown("""
    3. **Divisão por constante**:
    """)
    st.latex(r'''\Delta y = \frac{\Delta a}{k}''')

    st.markdown("""
    4. **Multiplicação/Divisão de grandezas**:
    """)
    st.latex(r'''\frac{\Delta y}{y} = \frac{\Delta a}{a} + \frac{\Delta b}{b} + \dots + \frac{\Delta n}{n}''')

    st.markdown("""
    5. **Potência**:
    """)
    st.latex(r'''\frac{\Delta y}{y} = n \cdot \frac{\Delta a}{a}''')
    
    st.write("""
    **PARTE EXPERIMENTAL**: 
             
    **Objetivos:**
             
     • (i) Realizar medidas diretas e indiretas,
             
     • (ii) expressar os resultados com suas respectivas incertezas e
             
     • (iii) conhecer o paquímetro, micrômetro, dinamômetro e o transferidor. 
                 
    **Material Utilizado:** Régua, paquímetro, micrômetro, dinamômetro, transferidor, bloco de madeira. 
    
    **Paquímetro:** Frequentemente utilizam-se para a medição de comprimento na indústria o 
    paquímetro, algumas vezes chamado de calibre, e o micrômetro também chamado de Palmer ou 
    parafuso micrométrico. 
    """)
    st.image(BytesIO(read_json("image.json", "image3.png")),
             caption="Figura 2 – Paquímetro de precisão 0,05 mm", use_container_width=True)
    st.write("""
    O paquímetro faz uso de uma escala auxiliar, chamada nônio ou vernier inferior, cujo 
    comprimento é de 9 vezes a menor divisão da escala principal, subdividida em 10 partes. A imagem 
    principal mostra as partes principais de um paquímetro. Ao fazer uma estimativa de um dado 
    comprimento 𝑙 lê-se a quantidade de milímetros na escala principal. Em seguida, procura-se qual 
    subdivisão do nônio coincide exatamente ao número de décimos de milímetro do comprimento 
    medido. Examine o detalhe da figura e observe que o comprimento 𝑙 medido é 24,70 𝑚𝑚. Como 
    precisão do paquímetro é 0,05 𝑚𝑚, então a medida deve ser apresentada como 𝑙 = 24,70±
    0,05 𝑚𝑚.
              
    **Micrômetro:** A Figura 3 mostra as partes principais de um micrômetro. Para cada avanço 
    de 1 𝑚𝑚 do deslocamento axial do tambor na escala da bainha, o tambor gira 1 volta. Dividindo-se 
    a circunferência 2𝜋𝑅 do tambor em 100 partes, cada divisão da escala do tambor será de 0,01 𝑚𝑚. 
    Portanto, a resolução do micrômetro da Figura 3 é de 0,01 𝑚𝑚. 
    """)
    st.image(BytesIO(read_json("image.json", "image4.png")),
             caption="Figura 3 – Micrômetro de resolução 0,01 mm", use_container_width=True)
    st.write("""O **dinamômetro** é um instrumento usado para medir força. Os modelos mais usuais 
    apresentam uma estrutura tubular, chamados dinamômetros tubulares, como o exemplo da Figura 
    4. Esses dinamômetros possuem escalas com divisões de 1/100  (um centésimo) de sua 
    capacidade máxima de carga (geralmente indicada no início do tubo da escala). Antes da utilização 
    do dinamômetro é necessário ajustá-lo através do parafuso liberador da capa, de modo a nivelar o 
    referencial (extremidade do tubo) com a marcação inicial da escala. 
    """)
    st.image(BytesIO(read_json("image.json", "image5.png")),
             caption="Figura 4 – Dinamômetro tubular", use_container_width=True)
    st.write("""
    Observe que no exemplo da Figura 4, a menor escala de medida é de 0,02 𝑁. Sendo assim, 
    a carga máxima suportada por esse instrumento é de 2,00 𝑁. Além disso, suas medidas possuem 
    incerteza de 0,01 𝑁. Ou seja, a leitura indicada no exemplo seria, portanto, de 1,30 ± 0,01 𝑁. 
    
    **ATENÇÃO:** seguem algumas recomendações importantes para **manutenção e conservação 
    do dinamômetro**
             
    • Nunca utilize o dinamômetro além da capacidade máxima indicada!
              
    • Nunca solte o dinamômetro bruscamente quando ele estiver distendido!
             
    A Figura 5 mostra um diagrama de um **transferidor semicircular (de 180º)**, que é um 
    instrumento usado para medir ou construir um ângulo de uma dada medida.  Existem transferidores 
    circulares, de 360º. Observe que em geral esses instrumentos possuem duas escalas de ângulos. 
    No exemplo da Figura 5, a escala interna é usada para medir ângulos no sentido horário e a escala 
    externa para medições no sentido anti-horário. 
    """)
    st.image(BytesIO(read_json("image.json", "image6.png")),
             caption="Figura 5 – Transferidor semicircular", use_container_width=True)
    st.write("""
    A Figura 6 mostra um exemplo de medida de ângulo entre as retas 𝑂𝐴 e 𝑂𝐵, que estão centradas 
    na origem ou vértice do transferidor (𝑂 ).Como de praxe, antes de realizar qualquer medida é 
    necessário verificar a menor escala do instrumento, que neste caso é de 1°. Portanto, a incerteza 
    da medida será de 0,5°. Observe que a reta 𝑂𝐴 está alinhada entre o vértice do transferidor e o 
    ângulo de 0°. A reta 𝑂𝐵 está alinhada entre o vértice e um ângulo de aproximadamente 58°. Como 
    não é possível ter certeza absoluta do valor medido devido a escala do transferidor, então podemos 
    dizer que neste caso o ângulo entre as retas é de 𝜃 = (58,0± 0,5)°. 
    """)
    st.image(BytesIO(read_json("image.json", "image7.png")),
             caption="Figura 6 – Medida de ângulo com transferidor", use_container_width=True)
def procedure_2_1() -> None:
    # Configurações para cada tipo de objeto
    config = {
        "Folha A4": {
            "artigo": "uma",
            "objeto": "da",
            "unidade": "cm",
            "A": 29.7,
            "B": 21.0,
            "C": 0.001,
            "paquimetro":0.05,
            "unit_paq": "mm",
            "C_paq":1.0,
            "num_folha":20,
            "micrometro":0.01,
            "C_mic":20.0,
        },
        "Bloco de Madeira": {
            "artigo": "um",
            "objeto": "do",
            "unidade": "mm",
            "A": 79.1,
            "B": 74.0,
            "C": 20.0,
            "paquimetro":0.05,
            "unit_paq": "mm",
            "C_paq":20.0,
            "micrometro":0.01,
            "C_mic":20.0,
        },
    }

    object_type = st.selectbox("Objeto de Estudo", list(config.keys()))
    cfg = config[object_type]
    
    st.markdown(f"**Procedimento 1 – Medida de A, B e C {cfg['objeto']} {object_type}**")
    st.write(f"1)Com a régua meça o comprimento (A) e a largura (B) de {cfg['artigo']} {object_type} com a régua.")
    st.write(f"Para medir a espessura (C) {cfg['objeto']} {object_type}, utilize o paquímetro.")

    if object_type == "Folha A4":
        st.write("""Como é impossível medir diretamente a espessura de uma única folha com o paquímetro, 
                 meça inicialmente a espessura de diversas folhas e divida o resultado pelo número de folhas.""")

    col1, col2, col3 = st.columns(3)
    A = float(col1.number_input(f"Comprimento A ({cfg['unidade']})", value=cfg["A"], step=0.01, format="%.4f", key=f"A_{object_type}"))
    B = float(col2.number_input(f"Largura B ({cfg['unidade']})", value=cfg["B"], step=0.01, format="%.4f", key=f"B_{object_type}"))
    C = float(col3.number_input(f"Espessura C ({cfg['unidade']})", value=cfg["C"], step=0.0001, format="%.4f", key=f"C_{object_type}"))

    if st.button("Calcular Volume"):
        volume = A * B * C
        st.success(f"Volume {cfg['objeto']} {object_type}: {volume:.4f} {cfg['unidade']}³")

    if st.button("Zerar"):
        st.rerun()

    st.write(f"""2) Tente medir diretamente a espessura {cfg['objeto']} {object_type} com o micrômetro. 
             Compare com o valor do paquímetro.""")
    col4,col5=st.columns(2)
    if object_type == "Folha A4":
        num_folhas=col4.number_input("Numero de folhas A4",value=cfg["num_folha"],step=1,key="num_folhas")
        med_paq=col5.number_input("Espessura das folhas",value=cfg["C_paq"],step=0.001,key="esp_folhas",format="%.3f")
        espessura_paq=float(col4.number_input(f"Espessura Paquímetro({cfg['unit_paq']})", value=float(num_folhas)/float(med_paq), step=0.0001, format="%.4f", key=f"C_paq_{object_type}")) 
    else:
        espessura_paq=float(col4.number_input(f"Espessura Paquímetro({cfg['unit_paq']})", value=cfg["C_paq"], step=0.0001, format="%.4f", key=f"C_paq_{object_type}")) 
    espessura_mic=float(col5.number_input(f"Espessura Micrômetro({cfg['unit_paq']})", value=cfg["C_mic"], step=0.0001, format="%.4f", key=f"C_mic_{object_type}"))
    st.write(f"A diferença entre as medidas é de {"{:.4f}".format(abs(espessura_paq - espessura_mic))} {cfg['unit_paq']}." if espessura_paq!=espessura_mic else "As medidas são iguais.")
    st.write(f"3) Determine o volume {cfg['objeto']} {object_type} e apresente com a incerteza.")
    col6,col7=st.columns(2)
    prec_paq=float(col6.number_input(f"Precisão Paquímetro({cfg['unit_paq']})", value=cfg["paquimetro"], step=0.0001, format="%.4f", key=f"prec_paq_{object_type}")) 
    prec_mic=float(col7.number_input(f"Precisão Micrômetro({cfg['unit_paq']})", value=cfg["micrometro"], step=0.0001, format="%.4f", key=f"prec_mic_{object_type}"))

def procedure_2_2():
    # Procedimento 2
    st.markdown("**Procedimento 2 – Dinamômetro**")
    st.write(
    """1) Identifique o valor da menor divisão da escala do dinamômetro e determine sua incerteza. 
    2) Fixe o bloco de madeira na extremidade do dinamômetro (suspenso verticalmente no tripé) e 
    determine o valor do peso do bloco. 
    """    
    )
    din_div = st.number_input("Menor divisão (N)", step=0.01)
    din_inc = din_div / 2
    peso_bloco = st.number_input("Peso do bloco (N)", step=0.01)
    
    col1,col2=st.columns(2)
    if col1.button("Calcular"):
        st.write(f"Incerteza: ±{din_inc:.2f} N")
    if col2.button("Zerar Valores"):
        st.rerun()
def procedure_2_3():
    # Procedimento 3
    st.markdown("**Procedimento 3 – Transferidor**")
    st.write("""
    1) Identifique o valor da menor divisão da escala do transferidor e determine sua incerteza. 
    2) Determine o valor do ângulo 𝜃 da figura abaixo: 
    """)
    # figura triangulo retângulo
    plot_triangulo()
    # st.image(BytesIO(read_json("image.json", "image8.png")),
            # caption="Figura 1 – Triângulo retângulo", use_container_width=True)

    transf_div = st.number_input("Menor divisão (°)", step=0.1)
    transf_inc = transf_div / 2
    angulo = st.number_input("Ângulo θ (°)", step=0.1)
    
    col1,col2=st.columns(2)
    if col1.button("Calcular"):
        st.write(f"Incerteza: ±{transf_inc:.2f}°")
    if col2.button("Zerar Valores"):
        st.rerun()
def procedure_2_4():
    op=st.selectbox("Exibição",["Padrão","Apêndice"])
    if op=="Padrão":
        procedure_2_4_a()
    elif op =="Apêndice":
        procedure_2_4_b()
    else:
        st.write("Aguardando escolha........")
def procedure_2_4_a():
    # Procedimento 4
    st.markdown("**Procedimento 4 – Caixa**")
    st.write("""1) Meça as dimensões A, B e C da caixa, conforme ilustrado na Figura 8. Utilize primeiro a régua 
    graduada em decímetro, depois em centímetro e finalmente em milímetro. Anote os resultados na      
    """)
    # figura cubo
    plot_caixa()
    # st.image(BytesIO(read_json("image.json", "image9.png")),
            # caption="Figura 1 – Cubo", use_container_width=True)
    st.write("Insira as dimensões A, B e C nas três escalas:")

    col_dm, col_cm, col_mm = st.columns(3)

    # Valores padrão para cada escala
    defaults = {
        "dm": [3.5, 2.4, 1.2],
        "cm": [35.4, 24.1, 13.0],
        "mm": [353.0, 247.0, 132.0]
    }

    # Associa escala às colunas
    colunas = {"dm": col_dm, "cm": col_cm, "mm": col_mm}

    # Criação dos inputs
    medidas = {}
    for escala in ["dm", "cm", "mm"]:
        col = colunas[escala]
        medidas[escala] = {}
        for letra, default_val in zip(["A", "B", "C"], defaults[escala]):
            medidas[escala][letra] = col.number_input(
                f"{letra} ({escala})",
                step=0.001,
                value=default_val
            )

    # Cálculo volume e desvios
    resultados = []
    desvio_valores_abs = {}
    st.write("Formula para obter o valor do desvio percentual:")
    st.latex(r"{Desvio} = \frac{incerteza}{medida} \times 100 \%")
    for escala, vals in medidas.items():
        A_, B_, C_ = vals["A"], vals["B"], vals["C"]
        volume = A_ * B_ * C_

        # meia divisão do instrumento (na mesma unidade da escala)
        inc = 0.5  

        # desvio percentual
        desv_percent = ((inc/A_) + (inc/B_) + (inc/C_)) * 100 if A_ and B_ and C_ else 0
        
        # desvio absoluto
        if volume > 0:
            #if volume >= 1000:
            expoente = int(math.log10(volume * desv_percent))
            valor = round((volume * desv_percent) / (10**expoente), 2)
            desvio_valores_abs[escala] = (valor, expoente)
            #else:
                #desvio_valores_abs[escala] = (round(volume * desv_percent, 2), None)
        else:
            desvio_valores_abs[escala] = (0, None)

        resultados.append([escala, volume, desv_percent])

    # Exibição tabela principal
    df_result = pd.DataFrame(resultados, columns=["Escala", "Volume", "Desvio Percentual (%)"])
    st.table(df_result)
    st.write("Formula para obter o valor do desvio pelo desvio percentual em notação cientifica:")
    st.latex(r"\frac{Volume \times Desvio}{\log_{10}(Volume \times Desvio)}")
    # Exibição dos desvios absolutos calculados automaticamente
    for escala, (valor, expoente) in desvio_valores_abs.items():
        if expoente is None:
            st.write(f"O desvio em {escala} é {valor}")
        else:
            st.write(f"O desvio em {escala} é {valor} × 10^{expoente} {escala}^{3}")
def procedure_2_4_b():
    # Valores padrão (dicionário aninhado)
    default_dados = {
        "Grupo 1": {
            "A": {"dm": 3.5, "cm": 35.0, "mm": 355.0},
            "B": {"dm": 2.4, "cm": 24.0, "mm": 242.0},
            "C": {"dm": 1.3, "cm": 13.1, "mm": 131.0}
        },
        "Grupo 2": {
            "A": {"dm": 3.5, "cm": 35.9, "mm": 357.0},
            "B": {"dm": 2.4, "cm": 24.9, "mm": 250.0},
            "C": {"dm": 1.3, "cm": 13.2, "mm": 134.0}
        },
        "Grupo 3": {
            "A": {"dm": 3.5, "cm": 35.4, "mm": 353.0},
            "B": {"dm": 2.4, "cm": 24.1, "mm": 247.0},
            "C": {"dm": 1.2, "cm": 13.0, "mm": 132.0}
        },
        "Grupo 4": {
            "A": {"dm": 3.5, "cm": 35.0, "mm": 354.0},
            "B": {"dm": 2.4, "cm": 24.7, "mm": 247.0},
            "C": {"dm": 1.3, "cm": 13.3, "mm": 129.0}
        }
    }

    # Sidebar para escolher modo de exibição
    opcoes_grupos = ["Todos"] + list(default_dados.keys())
    escolha = st.sidebar.selectbox("Selecione o grupo", opcoes_grupos)

    # Determinar grupos a exibir
    if escolha == "Todos":
        qtd_grupos = st.sidebar.slider("Quantidade de grupos", 1, 4, 4)
        grupos_para_exibir = list(default_dados.keys())[:qtd_grupos]
    else:
        grupos_para_exibir = [escolha]

    # Criar estrutura para armazenar valores editados
    dados_editados = {}

    # Exibir inputs para os grupos escolhidos
    for grupo_nome in grupos_para_exibir:
        st.subheader(grupo_nome)
        col_dm, col_cm, col_mm = st.columns(3)
        dados_editados[grupo_nome] = {}
        for letra in ["A", "B", "C"]:
            dados_editados[grupo_nome][letra] = {
                "dm": col_dm.number_input(f"{letra} (dm) - {grupo_nome}",
                                          value=default_dados[grupo_nome][letra]["dm"],
                                          step=0.001),
                "cm": col_cm.number_input(f"{letra} (cm) - {grupo_nome}",
                                          value=default_dados[grupo_nome][letra]["cm"],
                                          step=0.001),
                "mm": col_mm.number_input(f"{letra} (mm) - {grupo_nome}",
                                          value=default_dados[grupo_nome][letra]["mm"],
                                          step=0.001)
            }

    # Processar cálculos
    linhas = []
    for grupo, medidas in dados_editados.items():
        for escala in ["dm", "cm", "mm"]:
            A_ = medidas["A"][escala]
            B_ = medidas["B"][escala]
            C_ = medidas["C"][escala]
            volume = A_ * B_ * C_

            # meia divisão do instrumento
            inc = 0.5

            # desvio percentual
            desv_percent = ((inc/A_) + (inc/B_) + (inc/C_)) * 100 if A_ and B_ and C_ else 0

            # desvio absoluto (notação científica)
            if volume > 0 and desv_percent > 0:
                expoente = int(math.log10(volume * desv_percent))
                valor = round((volume * desv_percent) / (10**expoente), 2)
                desvio_abs_str = f"{valor} × 10^{expoente} {escala}³"
            else:
                desvio_abs_str = "0"

            linhas.append({
                "Grupo": grupo,
                "Escala": escala,
                "A": A_,
                "B": B_,
                "C": C_,
                "Volume": round(volume, 4),
                "Desvio Percentual (%)": round(desv_percent, 4),
                "Desvio Absoluto": desvio_abs_str
            })

    # DataFrame final
    df = pd.DataFrame(linhas)
    st.dataframe(df, hide_index=True)
    
    st.subheader("Fórmulas usadas")
    st.write("Formula para obter o valor do desvio percentual:")
    st.latex(r"{Desvio} = \frac{incerteza}{medida} \times 100 \%")
    st.write("Formula para obter o valor do desvio pelo desvio percentual em notação cientifica:")
    st.latex(r"\frac{Volume \times Desvio}{\log_{10}(Volume \times Desvio)}")

def activity_02():
   
    st.subheader("Procedimentos – Atividade 2")
    select_procedure=st.sidebar.selectbox("Procedimentos da Atividade",["Selecione o Procedimento",
                                                              "Procedimento 1",
                                                              "Procedimento 2",
                                                              "Procedimento 3",
                                                              "Procedimento 4",])
    if select_procedure=="Procedimento 1":
        procedure_2_1()
    elif select_procedure=="Procedimento 2":
        procedure_2_2()
    elif select_procedure=="Procedimento 3":
        procedure_2_3()
    elif select_procedure=="Procedimento 4":
        procedure_2_4()
    else:
        st.write("Aguardando escolha.......")    
    
def teoria():
       
    st.title("Conceitos Laboratório de Física")
    concept=st.sidebar.selectbox("Conceitos",["Selecione a Etapa","Conceitos - Atividade 1",
                                    "Conceitos - Atividade 2",
                                    "Conceitos - Atividade 3",
                                    "Conceitos - Atividade 4"])
    if concept=="Conceitos - Atividade 1":
        stage1=st.selectbox("Temas",["Selecione a Etapa",
                                     "INTRODUÇÃO",
                                     "MEDIÇÕES E INCERTEZAS"])
        if stage1=="INTRODUÇÃO":
            Introduction()
        elif stage1=="MEDIÇÕES E INCERTEZAS":
            concept_01()
        else:
            st.write("Aguardando escolha.......")
    elif concept=="Conceitos - Atividade 2":
        concept02()
    else:
        st.write("Aguardando escolha.......")
def activity_01():
    st.subheader("Análise de Medições de Tempo de Queda")
    st.write("Insira 10 medições do tempo de queda de uma esfera para calcular o tempo médio, a incerteza e o desvio médio percentual.")

    # Entrada de 10 valores de tempo de queda com valores iniciais do arquivo Atividade1_em_sala.py.txt
    st.header("Medições de Tempo de Queda")
    col1,col2,col3=st.columns(3)
    with col1:
        t1 = st.number_input("Medição 1 (s)", step=0.01, format="%.5f", value=0.47)
        t4 = st.number_input("Medição 4 (s)", step=0.01, format="%.5f", value=0.41)
        t7 = st.number_input("Medição 7 (s)", step=0.01, format="%.5f", value=0.15)
        t10 = st.number_input("Medição 10 (s)", step=0.01, format="%.5f", value=0.35)
    with col2:
        t2 = st.number_input("Medição 2 (s)", step=0.01, format="%.5f", value=0.25)
        t5 = st.number_input("Medição 5 (s)", step=0.01, format="%.5f", value=0.41)
        t8 = st.number_input("Medição 8 (s)", step=0.01, format="%.5f", value=0.13)
        
    with col3:
        t3 = st.number_input("Medição 3 (s)", step=0.01, format="%.5f", value=0.61)
        t6 = st.number_input("Medição 6 (s)", step=0.01, format="%.5f", value=0.28)
        t9 = st.number_input("Medição 9 (s)", step=0.01, format="%.5f", value=0.41)
        

    # Lista com as 10 medições
    t_list = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

    # Cálculo do tempo médio (t_med) sem arredondamento intermediário
    # O tempo mais provável para o tempo de queda é a média aritmética.
    t_med = col2.number_input("Média Aritmética (s)", step=0.01, format="%.5f", value=sum(t_list) / len(t_list))
    # Cálculo da incerteza (Delta_t) sem arredondamento intermediário
    # A incerteza (Δt) é identificada com o desvio padrão.
    # A fórmula é: $\Delta t=\frac{1}{n}\sum_{i=1}^{n}|t_{med}-t_{i}|.$.
    delta_t = col3.number_input("Desvio Padrão (s)", step=0.01, format="%.5f", value=(sum(abs(t_med - t_i) for t_i in t_list))/ len(t_list))
    


    # Cálculo do desvio médio percentual (epsilon)
    # O desvio médio percentual é definido como $\epsilon=\frac{\Delta t}{t_{med}}\times100.$.
    if t_med != 0:

        col4,col5=st.columns([0.6,0.4])
        col4.subheader("Resultados detalhados em tabela:")
        df = pd.DataFrame(t_list, index=range(1, len(t_list) + 1), columns=['Tempo (s)'])
        df['Desvio (Tempo (s) - Média (s))']=abs(df['Tempo (s)'] - t_med)
        col4.dataframe(df)
        
        col5.subheader("Observações acerca do Desvio Percentual:")
        epsilon = (delta_t / t_med) * 100
        col5.write(f"Desvio médio percentual ($\\epsilon$): {epsilon:.5f} %")
        col5.write("O resultado com menor desvio médio percentual é o mais preciso.")
        
        # Apresentação dos resultados formatados com 5 casas decimais
        col5.header("Resultados")
        col5.write(f"Tempo médio ($t_{{med}}$): {t_med:.5f} s")
        col5.write(f"Incerteza ($\\Delta t$): {delta_t:.5f} s")
        col5.write(f"O resultado da medição é: $({t_med:.5f} \\pm {delta_t:.5f})$ s")
        col5.write("A forma mais comum de se expressar o resultado da medição de uma grandeza x é $(x\\pm\\Delta x)$ [unidade].")
        
        st.subheader("Tempo médio de reação, desvio médio e incerteza de cada grupo.")
        col6,col7,col8=st.columns([0.3,0.3,0.4])
        with col6:
            t_med_g1=st.number_input("Média Grupo 1 (s)", step=0.01, format="%.5f", value=0.285)
            t_med_g2=st.number_input("Média Grupo 2 (s)", step=0.01, format="%.5f", value=0.289)
            t_med_g3=st.number_input("Média Grupo 3 (s)", step=0.01, format="%.5f", value=t_med)
            t_med_g4=st.number_input("Média Grupo 4 (s)", step=0.01, format="%.5f", value=0.293)
        with col7:   
            delta_t_g1=st.number_input("Desvio Grupo 1 (s)", step=0.01, format="%.5f", value=0.285)
            delta_t_g2=st.number_input("Desvio Grupo 2 (s)", step=0.01, format="%.5f", value=0.289)
            delta_t_g3=st.number_input("Desvio Grupo 3 (s)", step=0.01, format="%.5f", value=delta_t)
            delta_t_g4=st.number_input("Desvio Grupo 4 (s)", step=0.01, format="%.5f", value=0.293)
            
        t_list_med=[t_med_g1,t_med_g2,t_med_g3,t_med_g4]
        delta_t_list=[delta_t_g1,delta_t_g2,delta_t_g3,delta_t_g4]
        epsilon_list=list((delta_t_g/t_med_g)*100 for t_med_g ,delta_t_g in zip(t_list_med,delta_t_list))
        
        data = {
            'Grupo':["Grupo 1","Grupo 2","Grupo 3","Grupo 4"],
            'Tempo Médio (s)': t_list_med,
            'Desvio (s)': delta_t_list
        }
        data2= {
            'Grupo':["Grupo 1","Grupo 2","Grupo 3","Grupo 4"],
            'Desvio Percentual (%)':epsilon_list
        }
        # Create the DataFrame
        col8.dataframe(pd.DataFrame(data).style.format(precision=5),hide_index=True)
        col8.dataframe(pd.DataFrame(data2).style.format(precision=5),hide_index=True)
    else:
        st.write("Não é possível calcular o desvio médio percentual e outros cálculos com tempo médio zero.")

def atividades():
    st.title("Atividades Laboratório de Física")
    act=st.sidebar.selectbox("Atividades",["Selecione a Atividade",
                                   "Atividade 1",
                                    "Atividade 2",
                                    "Atividade 3",
                                    "Atividade 4"])
    if act=="Atividade 1":
        activity_01()
    elif act=="Atividade 2":
        activity_02()
    else:
        st.write("Aguardando escolha.......")
def laboratorio():
    st.sidebar.title("Conceitos e Atividades - Laboratório de Física")
    option=st.sidebar.selectbox("Temas",["Selecione o Tema","Conceitos","Atividades"])
    if option=="Conceitos":
        teoria()
    elif option=="Atividades":
        atividades()
    else:
        st.write("Aguardando escolha.......")
if __name__ == "__main__":
    #test()
    laboratorio()
