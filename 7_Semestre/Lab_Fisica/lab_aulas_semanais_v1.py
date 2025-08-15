# Aula 12-08-2025 protótipo 
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

if __name__ == "__main__":
    st.sidebar.header("Aulas Práticas – Laboratório de Física")
    
    set_aula=st.sidebar.selectbox("Aulas",["Selecione uma aula","Atividade 1","Atividade 2"])
    
    if set_aula=="Atividade 1":
        st.write("Aguardando aprovação")
    elif set_aula=="Atividade 2":
        activity_02()
    else:
        st.write("Aguardando escolha......")
