# Aula 11-08-2025 protótipo 

import streamlit as st
import pandas as pd
import numpy as np

def procedure_2_1():
    # Procedimento 1
    st.markdown("**Procedimento 1 – Medida de A, B e C da folha A4**")
    st.write("""1) Com a régua meça o comprimento (A) e a largura (B) de uma folha de papel A4. Para medir a 
    espessura (C) da folha utilize o paquímetro. Como é impossível medir diretamente a espessura de 
    uma única folha com o paquímetro, meça inicialmente a espessura de diversas folhas e divida o 
    resultado pelo número de folhas.   
    Escreva os resultados com as incertezas."""
    )
    col1, col2, col3 = st.columns(3)
    A = col1.number_input("Comprimento A (cm)",value=29.7, step=0.01,format='%.2f',key="A")
    B = col2.number_input("Largura B (cm)",value=21.0,step=0.01,format='%.2f',key="B")
    C = col3.number_input("Espessura C (cm)",value=0.001, step=0.0001,format='%.4f',key="C")

    if col1.button("Calcular"):
        st.write(f"Volume da folha: {(A*B*C):.4f} cm³")
    if col2.button("Zerar Volume"):
        st.rerun()
        
    st.write(
    """2) Tente medir diretamente a espessura da folha com o micrômetro. Compare o resultado com 
    aquele encontrado com o paquímetro.""")
    st.write(
    """3) Determine o volume da folha e escreva o resultado com a incerteza. 
    """    
    )
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

    medidas = {}
    for escala, col in zip(["dm", "cm", "mm"], [col_dm, col_cm, col_mm]):
        medidas[escala] = {
            "A": col.number_input(f"A ({escala})", step=0.001),
            "B": col.number_input(f"B ({escala})", step=0.001),
            "C": col.number_input(f"C ({escala})", step=0.001)
        }

    # Cálculo volume e desvios
    resultados = []
    for escala, vals in medidas.items():
        A_, B_, C_ = vals["A"], vals["B"], vals["C"]
        volume = A_ * B_ * C_
        inc_A = (0.5 / (10 if escala == "cm" else (1 if escala == "dm" else 1000)))
        inc_B = inc_A
        inc_C = inc_A
        desv_percent = ((inc_A/A_) + (inc_B/B_) + (inc_C/C_)) * 100 if A_ and B_ and C_ else 0
        resultados.append([escala, volume, desv_percent])

    df_result = pd.DataFrame(resultados, columns=["Escala", "Volume", "Desvio Percentual (%)"])
    st.table(df_result)
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
